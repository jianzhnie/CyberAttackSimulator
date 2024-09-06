import torch
import torch_npu
import torch.nn.functional as F
from torch import nn
from torch.optim import Adam

from algorithms.GAIL_and_AIRL.gail_airl_ppo.algo.discrete import GAILDiscrim

from .ppo_discrete import PPO
torch.set_warn_always(False)
from torch_npu.contrib import transfer_to_npu


class GAIL(PPO):

    def __init__(self, buffer_exp, state_dim, action_dim, device, seed,
                    gamma=0.995, rollout_length=50000, mix_buffer=1,
                    batch_size=64, lr_actor=3e-4, lr_critic=3e-4, lr_disc=3e-4,
                    units_actor=(64, 64), units_critic=(64, 64),
                    units_disc=(100, 100), epoch_ppo=50, epoch_disc=10,
                    clip_eps=0.2, lambd=0.97, ent_coef=0.0, max_grad_norm=10.0,
                    save_interval=1e5, eval_interval=10000, num_eval_eps=100, net_width=64,
                    l2_reg=1e-3, adv_norm=False, ent_coef_decay=0.99
                 ):
        super().__init__(
            state_dim=state_dim,
            action_dim=action_dim,
            rollout_length=rollout_length,
            save_interval=save_interval,
            eval_interval=eval_interval,
            num_eval_episodes=num_eval_eps,
            gamma=gamma,
            lambd=lambd,
            net_width=net_width,
            lr_actor=lr_actor,
            lr_critic=lr_critic,
            clip_eps=clip_eps,
            epoch_ppo=epoch_ppo,
            batch_size=batch_size,
            l2_reg=l2_reg,
            entropy_coef=ent_coef,
            adv_normalization=adv_norm,
            entropy_coef_decay=ent_coef_decay,
            device=device,
            mix_buffer=mix_buffer,
        )

        # Expert's buffer.
        self.buffer_exp = buffer_exp

        # Discriminator.
        self.disc = GAILDiscrim(
            state_dim=state_dim,
            action_dim=1, # 离散空间的话，action_dim虽然为41，但是保存的是一个数，不是one-hot编码
            hidden_units=units_disc,
            hidden_activation=nn.Tanh()
        ).to(device)

        self.learning_steps_disc = 0
        self.optim_disc = Adam(self.disc.parameters(), lr=lr_disc)
        self.batch_size = batch_size
        self.epoch_disc = epoch_disc

    def update(self, writer):
        self.learning_steps += 1

        for _ in range(self.epoch_disc):
            self.learning_steps_disc += 1

            # Samples from current policy's trajectories.
            states, actions = self.buffer.sample(self.batch_size)[:2]
            # Samples from expert's demonstrations.
            states_exp, actions_exp = self.buffer_exp.sample(self.batch_size)[:2]
            # Update discriminator.
            self.update_disc(states, actions, states_exp, actions_exp, writer)

        # We don't use reward signals here,
        states, actions, _, next_states, log_pis, state_values, dones = self.buffer.get()

        # Calculate rewards.
        rewards = self.disc.calculate_reward(states, actions)

        # Update PPO using estimated rewards.
        self.update_ppo(states, actions, rewards, log_pis, state_values)

    def update_disc(self, states, actions, states_exp, actions_exp, writer):
        # Output of discriminator is (-inf, inf), not [0, 1].
        logits_pi = self.disc(states, actions)
        logits_exp = self.disc(states_exp, actions_exp)

        # Discriminator is to maximize E_{\pi} [log(1 - D)] + E_{exp} [log(D)].
        loss_pi = -F.logsigmoid(-logits_pi).mean()
        loss_exp = -F.logsigmoid(logits_exp).mean()
        loss_disc = loss_pi + loss_exp

        self.optim_disc.zero_grad()
        loss_disc.backward()
        self.optim_disc.step()

        if self.learning_steps_disc % self.epoch_disc == 0:
            writer.add_scalar('loss/disc', loss_disc.item(), self.learning_steps)

            # Discriminator's accuracies.
            with torch.no_grad():
                acc_pi = (logits_pi < 0).float().mean().item()
                acc_exp = (logits_exp > 0).float().mean().item()
            print(f"Discriminator loss: {round(loss_disc.item(), 4)}  | Accuracy exp: {round(acc_exp, 4)}   | Accuracy pi: {round(acc_pi, 4)} |")
            writer.add_scalar('stats/acc_pi', acc_pi, self.learning_steps)
            writer.add_scalar('stats/acc_exp', acc_exp, self.learning_steps)