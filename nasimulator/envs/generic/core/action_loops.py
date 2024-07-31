"""The ``ActionLoop`` class helps reduce boilerplate code when evaluating an
agent within a target environment.

Serves a similar function to library helpers such as Stable Baselines 3
``evaluate_policy()".
"""

import os
import re
from datetime import datetime
from pathlib import Path
from threading import Thread
from typing import Any, List, Optional
from uuid import uuid4

import imageio
import matplotlib.pyplot as plt
import moviepy.editor as mp
import pandas as pd
from yawning_titan import APP_IMAGES_DIR, IMAGES_DIR, VIDEOS_DIR
from yawning_titan.envs.generic.generic_env import GenericNetworkEnv


class ActionLoop:
    """A class that represents different post-training action loops for
    agents."""

    def __init__(
        self,
        env: GenericNetworkEnv,
        agent: Any,
        filename: Optional[str] = None,
        episode_count: Optional[int] = None,
    ) -> None:
        """Initialize the ActionLoop class.

        Args:
            env: The environment to run through.
            agent: The agent to run in the environment.
            filename: The save name for the action loop.
            episode_count: The number of episodes to go through.
        """
        self.env: GenericNetworkEnv = env
        self.agent = agent
        self.filename = filename if filename is not None else str(uuid4())
        self.episode_count = episode_count

    def gif_action_loop(
        self,
        render_network: bool = True,
        prompt_to_close: bool = False,
        save_gif: bool = False,
        save_webm: bool = False,
        deterministic: bool = False,
        gif_output_directory: Optional[Path] = None,
        webm_output_directory: Optional[Path] = None,
        *args,
        **kwargs,
    ) -> List[pd.DataFrame]:
        """Run the agent in evaluation and create a GIF from episodes.

        Args:
            render_network: Toggle rendering on or off. Default is True.
            prompt_to_close: Toggle if the output window should close immediately on loop ending. Default is False.
            save_gif: Toggle if GIF file should be saved. Default is False.
            save_webm: Toggle if WebM file should be saved. Default is False.
            deterministic: Toggle if the agent's actions should be deterministic. Default is False.
            gif_output_directory: Directory where the GIF will be output. Default is None.
            webm_output_directory: Directory where the WebM file will be output. Default is None.

        Returns:
            A list of DataFrames containing the results of each episode.
        """
        gif_uuid = str(uuid4())

        complete_results = []
        for i in range(self.episode_count):
            # temporary log to satisfy repeatability tests until logging can be full implemented
            results = pd.DataFrame(columns=['action', 'rewards', 'info'])
            obs = self.env.reset()
            done = False
            frame_names = []
            current_image = 0

            while not done:
                # gets the agents prediction for the best next action to take
                action, _states = self.agent.predict(
                    obs, deterministic=deterministic)
                # TODO: setup logging properly here
                # logging.info(f'Blue Agent Action: {action}')
                # step the env
                obs, rewards, done, info = self.env.step(action)
                results.loc[len(results.index)] = [action, rewards, info]
                # TODO: setup logging properly here
                # logging.info(f'Observations: {obs.flatten()} Rewards:{rewards} Done:{done}')
                # self.env.render(episode=i+1)

                if save_gif or save_webm:
                    current_name = os.path.join(
                        APP_IMAGES_DIR, f'{gif_uuid}_{current_image}.png')
                    current_image += 1

                    # set the size of the gif image
                    self._get_render_figure(current_name)

                    frame_names.append(current_name)

                if render_network:
                    self.env.render(*args, **kwargs)

            # get current time
            string_time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

            generate_render_thread = []

            def natural_sort_key(
                s: str, _nsre=re.compile('([0-9]+)')) -> List[Any]:
                return [
                    int(text) if text.isdigit() else text.lower()
                    for text in _nsre.split(s)
                ]

            frame_names = sorted(frame_names, key=natural_sort_key)

            if save_gif:
                if gif_output_directory is None:
                    gif_output_directory = IMAGES_DIR
                if not os.path.exists(gif_output_directory):
                    os.makedirs(gif_output_directory)
                gif_path = os.path.join(
                    gif_output_directory,
                    f'{self.filename}_{string_time}_{self.episode_count}.gif',
                )

                # gif generator thread
                gif_thread = Thread(target=self.generate_gif,
                                    args=(gif_path, frame_names))

                generate_render_thread.append(gif_thread)

            if save_webm:
                if webm_output_directory is None:
                    webm_output_directory = VIDEOS_DIR
                if not os.path.exists(webm_output_directory):
                    os.makedirs(webm_output_directory)
                webm_path = os.path.join(
                    webm_output_directory,
                    f'{self.filename}_{string_time}_{self.episode_count}.mp4',
                )

                # video generator thread
                video_thread = Thread(target=self.generate_webm,
                                      args=(webm_path, frame_names))
                generate_render_thread.append(video_thread)
            # if any threads were added to generate threads list, run them
            if generate_render_thread:
                for thread in generate_render_thread:
                    thread.start()
                    thread.join()
                # clean up once done
                self.render_cleanup(frame_names)

            complete_results.append(results)

        if not prompt_to_close:
            self.env.close()
        return complete_results

    def standard_action_loop(self,
                             deterministic: bool = False
                             ) -> List[pd.DataFrame]:
        """Indefinitely act within the environment using a trained agent.

        Args:
            deterministic: Toggle if the agent's actions should be deterministic. Default is False.

        Returns:
            A list of DataFrames containing the results of each episode.
        """
        complete_results = []
        for i in range(self.episode_count):
            # temporary log to satisfy repeatability tests until logging can be full implemented
            results = pd.DataFrame(columns=['action', 'rewards', 'info'])
            obs = self.env.reset()
            done = False
            while not done:
                action, _states = self.agent.predict(
                    obs, deterministic=deterministic)
                # TODO: setup logging properly here
                # logging.info(f'Blue Agent Action: {action}')
                obs, rewards, done, info = self.env.step(action)
                results.loc[len(results.index)] = [action, rewards, info]
            complete_results.append(results)
        return complete_results

    def random_action_loop(self, deterministic: bool = False) -> None:
        """Indefinitely act within the environment taking random actions.

        Args:
            deterministic: Toggle if the agent's actions should be deterministic. Default is False.
        """
        for i in range(self.episode_count):
            obs = self.env.reset()
            done = False
            reward = 0
            while not done:
                action = self.agent.predict(obs,
                                            reward,
                                            done,
                                            deterministic=deterministic)
                ob, reward, done, ep_history = self.env.step(action)
                if done:
                    break

    @classmethod
    def _get_render_figure(cls, gif_name: str) -> Any:
        """Save the current plot figure as an image.

        Args:
            gif_name: The filename for the image.

        Returns:
            The current figure.
        """
        fig = plt.gcf()
        # save the current image
        plt.savefig(gif_name, bbox_inches='tight', dpi=100)
        return fig

    def generate_gif(self, gif_path: str, frame_names: List[str]) -> None:
        """Generate GIF from images.

        Args:
            gif_path: The path where the generated GIF will be saved.
            frame_names: A list of file paths to the images that will be used as frames in the GIF.
        """
        # TODO: Full docstring.
        with imageio.get_writer(gif_path, mode='I') as writer:
            # create a gif from the images
            for frame_num, filename in enumerate(frame_names):
                # skip first frame because it is empty
                if filename == frame_names[0]:
                    continue
                # read image
                image = imageio.imread(filename)
                # add image to GIF
                writer.append_data(image)

                # if the last frame, add more of it so the result can be seen longer
                if frame_num == len(frame_names) - 1:
                    for _ in range(10):
                        writer.append_data(image)

    def generate_webm(self,
                      webm_path: str,
                      frame_names: List[str],
                      fps: int = 1) -> None:
        """Create a WebM video from a sequence of image files.

        Args:
            webm_path: The path where the generated WebM file will be saved.
            frame_names: A list of file paths to the images that will be used as frames in the video.
            fps: Frames per second for the video. Default is 5.
        """
        # Create a video clip from the image sequence
        clip = mp.ImageSequenceClip(frame_names[1:], fps=fps)

        # Write the video clip to a WebM file
        clip.write_videofile(webm_path, codec='mpeg4')

    def render_cleanup(self, frame_names: List[str]) -> None:
        """Delete the frame image files.

        Args:
            frame_names: A list of file paths to the images that were used as frames.
        """
        for filename in set(frame_names):
            os.remove(filename)
