from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

from sklearn.model_selection import train_test_split

from sklearn.metrics import (accuracy_score,
                             confusion_matrix,
                             mean_squared_error,
                             r2_score,
                             mean_absolute_error,
                             log_loss,
                             precision_score,
                             recall_score)
import dvc.api
import io
import mlflow
import time
from cleaner import CleanDataFrame

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from logger import logger

class TrainingPipeline(Pipeline):
    '''
    Class -> TrainingPipeline, ParentClass -> Sklearn-Pipeline
    Extends from Scikit-Learn Pipeline class. Additional functionality to track 
    model metrics and log model artifacts with mlflow
    params:
    steps: list of tuple (similar to Scikit-Learn Pipeline class)
    '''

    def __init__(self, steps):
        super().__init__(steps)

    def fit(self, X_train, y_train):
        try:
            self.__pipeline = super().fit(X_train, y_train)
            return self.__pipeline
        except Exception as e:
            logger.error(e)
        

    def get_metrics(self, y_true, y_pred, y_pred_prob):
        try:
            acc = accuracy_score(y_true, y_pred)
            prec = precision_score(y_true, y_pred)
            recall = recall_score(y_true, y_pred)
            entropy = log_loss(y_true, y_pred_prob)
            cm = confusion_matrix(y_true, y_pred)
            true_pos = cm[0][0]
            true_neg = cm[1][1]
            false_pos = cm[0][1]
            false_neg = cm[1][0]

            return {
                'accuracy': round(acc, 2),
                'precision': round(prec, 2),
                'recall': round(recall, 2),
                'entropy': round(entropy, 2),
                'true_pos': true_pos,
                'true_neg': true_neg,
                'false_pos': false_pos,
                'false_neg': false_neg,
            }
        except Exception as e:
            logger.error(e)
            return {}

    def get_feature_importance(self, model, x):
        try: 
            feature_importance = None
            if str(model) == "LogisticRegression()":
                feature_importance = model.coef_[0]
            else:
                feature_importance = model.feature_importances_
            feature_array = {}
            for i, v in enumerate(feature_importance):
                feature_array[x.columns[i]] = v
            return feature_array
        except Exception as e:
            logger.error(e)
            return []
        

    def make_model_name(self, experiment_name, run_name):
        try:
            clock_time = time.ctime().replace(' ', '-')
            return experiment_name + '_' + run_name + '_' + clock_time
        except Exception as e:
            logger.error(e)


    def log_model(self, model_key, X_test, y_test, experiment_name, run_name, run_params=None):
        try:
            model = self.__pipeline.get_params()[model_key]
            y_pred = self.__pipeline.predict(X_test)
            y_pred_prob = self.__pipeline.predict_proba(X_test)
            run_metrics = self.get_metrics(y_test, y_pred, y_pred_prob)
            feature_importance = self.get_feature_importance(
                model, X_test)
            feature_importance_plot = self.plot_feature_importance(
                feature_importance)
            pred_plot = self.plot_preds(y_test, y_pred, experiment_name)
            cm_plot = self.plot_confusion_matrix(y_test, y_pred)
            print(run_metrics)
            print(feature_importance)
            try:
                mlflow.set_experiment(experiment_name)
                mlflow.set_tracking_uri('http://localhost:5000')
                with mlflow.start_run(run_name=run_name):
                    if run_params:
                        for name in run_params:
                            mlflow.log_param(name, run_params[name])
                    for name in run_metrics:
                        mlflow.log_metric(name, run_metrics[name])

                    mlflow.log_param("columns", X_test.columns.to_list())
                    mlflow.log_figure(pred_plot, "predictions_plot.png")
                    mlflow.log_figure(cm_plot, "confusion_matrix.png")
                    mlflow.log_figure(feature_importance_plot,
                                    "feature_importance.png")
                    pred_plot.savefig("../images/predictions_plot.png")
                    cm_plot.savefig("../images/confusion_matrix.png")
                    feature_importance_plot.savefig("../images/feature_importance.png")
                    mlflow.log_dict(feature_importance, "feature_importance.json")

                model_name = self.make_model_name(experiment_name, run_name)
                mlflow.sklearn.log_model(
                    sk_model=self.__pipeline, artifact_path='models', registered_model_name=model_name)
            except Exception as e:
                logger.error(e)
            print('Run - %s is logged to Experiment - %s' %
                (run_name, experiment_name))
            return run_metrics
        except Exception as e:
            logger.error(e)
            return {}

    def plot_preds(self, y_test, y_preds, model_name):
        try:
            N = len(y_test)
            figure = plt.figure(figsize=(10, 5))
            original = plt.scatter(np.arange(1, N+1), y_test, c='blue')
            prediction = plt.scatter(np.arange(1, N+1), y_preds, c='red')
            plt.xticks(np.arange(1, N+1))
            plt.xlabel('# Oberservation', fontsize=30)
            plt.ylabel('REsponse', fontsize=25)
            title = 'True labels vs. Predicted Labels ({})'.format(model_name)
            plt.title(title, fontsize=25)
            plt.legend((original, prediction),
                    ('Original', 'Prediction'), fontsize=20)
            plt.show()
            logger.info("plotted prediction vs true labels")
            return figure
        except Exception as e:
            logger.error(e)

    def plot_confusion_matrix(self, actual, y_preds):
        # plot_confusion_matrix(model, actual, y_preds)
        # plt.show()
        try:
            figure = plt.figure(figsize=(12, 8))
            conf_matrix = confusion_matrix(actual, y_preds)
            sns.heatmap(conf_matrix / np.sum(conf_matrix), annot=True, fmt='.2%')
            plt.title('Confusion matrix', fontsize=30, fontweight='bold')
            plt.ylabel('True Label', fontsize=25)
            plt.xlabel('Predicted Label', fontsize=25)
            plt.show()
            logger.info("confusion matrix plotted")
            return figure
        except Exception as e:
            logger.error(e)
        

    def plot_feature_importance(self, feature_importance):
        try:
            importance = pd.DataFrame({
                'features': feature_importance.keys(),
                'importance_score': feature_importance.values()
            })
            fig = plt.figure(figsize=[12, 8])
            ax = sns.barplot(x=importance['features'],
                            y=importance['importance_score'])
            ax.set_title("Feature's importance")
            ax.set_xlabel("Features", fontsize=20)
            ax.set_ylabel("Importance", fontsize=20)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
            logger.info("feature importnace plotted")
            # ax.show()
            # figure = ax.get_figure()
            return fig
        except Exception as e:
            logger.error(e)


def label_encoder(x):
    try:
        lb = LabelEncoder()
        cat_cols = CleanDataFrame.get_categorical_columns(x)
        for col in cat_cols:
            x[col] = lb.fit_transform(x[col])
    except Exception as e:
            logger.error(e)
    return x


def get_pipeline(model, x):
    try:
        cat_cols = CleanDataFrame.get_categorical_columns(x)
        num_cols = CleanDataFrame.get_numerical_columns(
            x)   # Remove the target column

        categorical_transformer = Pipeline(steps=[
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])
        numerical_transformer = Pipeline(steps=[
            ('scale', StandardScaler())
        ])

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numerical_transformer, num_cols),
                # ('cat', categorical_transformer, cat_cols)
            ])
        train_pipeline = TrainingPipeline(steps=[
            ('preprocessor', preprocessor),
            ('model', model)
        ])

        return train_pipeline
    except Exception as e:
            logger.error(e)


def dvc_get_data(path, version='72d1bf77e90769aaef56e18685215ddc98af3343'):
    try:
        repo = "../"
        content = dvc.api.read(path=path,
                            repo=repo,
                            rev=version)
        df = pd.read_csv(io.StringIO(content), sep=",")

        return df
    except Exception as e:
            logger.error(e)
            return pd.DataFrame()


def run_train_pipeline(model, x, y, experiment_name, run_name):
    '''
    function which executes the training pipeline
    Args:
        model : an sklearn model object
        x : features dataframe
        y : labels
        experiment_name : MLflow experiment name
        run_name : Set run name inside each experiment
    '''
    try:
        x = label_encoder(x)
        train_pipeline = get_pipeline(model, x)

        X_train, X_test, y_train, y_test = train_test_split(x, y,
                                                            test_size=0.3,
                                                            random_state=123)
        run_params = model.get_params()

        train_pipeline.fit(X_train, y_train)
        return train_pipeline.log_model('model', X_test, y_test, experiment_name, run_name, run_params=run_params)
    except Exception as e:
            logger.error(e)
            return False
    
