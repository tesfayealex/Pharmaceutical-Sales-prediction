import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from logger import logger


class Plotter:
    def plot_hist(self, df: pd.DataFrame, column: str, color: str) -> None:
        # plt.figure(figsize=(15, 10))
        # fig, ax = plt.subplots(1, figsize=(12, 7))
        try:
            sns.displot(data=df, x=column, color=color,
                        kde=True, height=7, aspect=2)
            plt.title(f'Distribution of {column}', size=20, fontweight='bold')
            plt.show()
            logger.info(f'successfully displayed histogram plot')
        except Exception as e:
            logger.error(e)

    def plot_count(self, df: pd.DataFrame, column: str) -> None:
        try:
            plt.figure(figsize=(12, 7))
            sns.countplot(data=df, x=column)
            plt.title(f'Distribution of {column}', size=20, fontweight='bold')
            plt.show()
            logger.info(f'successfully displayed count plot')
        except Exception as e:
            logger.error(e)

    def plot_bar(self, df: pd.DataFrame, x_col: str, y_col: str, title: str, xlabel: str, ylabel: str) -> None:
        try:
            plt.figure(figsize=(12, 7))
            sns.barplot(data=df, x=x_col, y=y_col)
            plt.title(title, size=20)
            plt.xticks(rotation=75, fontsize=14)
            plt.yticks(fontsize=14)
            plt.xlabel(xlabel, fontsize=16)
            plt.ylabel(ylabel, fontsize=16)
            plt.show()
            logger.info(f'successfully displayed bar plot')
        except Exception as e:
            logger.error(e)

    def plot_heatmap(self, df: pd.DataFrame, title: str, cbar=False) -> None:
        try:
            plt.figure(figsize=(12, 7))
            sns.heatmap(df, annot=True, cmap='viridis', vmin=0,
                        vmax=1, fmt='.2f', linewidths=.7, cbar=cbar)
            plt.title(title, size=18, fontweight='bold')
            plt.show()
            logger.info(f'successfully displayed heatmap plot')
        except Exception as e:
            logger.error(e)

    def plot_box(self, df: pd.DataFrame, x_col: str, title: str) -> None:
        try:
            plt.figure(figsize=(12, 7))
            sns.boxplot(data=df, x=x_col)
            plt.title(title, size=20)
            plt.xticks(rotation=75, fontsize=14)
            plt.show()
            logger.info(f'successfully displayed box plot')
        except Exception as e:
            logger.error(e)

    def plot_box_multi(self, df: pd.DataFrame, x_col: str, y_col: str, title: str) -> None:
        try:
            plt.figure(figsize=(12, 7))
            sns.boxplot(data=df, x=x_col, y=y_col)
            plt.title(title, size=20)
            plt.xticks(rotation=75, fontsize=14)
            plt.yticks(fontsize=14)
            plt.show()
            logger.info(f'successfully displayed box multi plot')
        except Exception as e:
            logger.error(e)

    def plot_scatter(self, df: pd.DataFrame, x_col: str, y_col: str, title: str,) -> None:
        try:
            plt.figure(figsize=(12, 7))
            sns.scatterplot(data=df, x=x_col, y=y_col)
            plt.title(title, size=20)
            plt.xticks(fontsize=14)
            plt.yticks(fontsize=14)
            plt.show()
            logger.info(f'successfully displayed scatter plot')
        except Exception as e:
            logger.error(e)
