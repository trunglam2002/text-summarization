from text_summarizer.components.model_trainer import ModelTrainer
from text_summarizer.config.configuration import ConfigurationManager


class ModelTrainerTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config = ConfigurationManager()
            model_trainer_config = config.get_model_trainer_config()
            model_trainer = ModelTrainer(
                config=model_trainer_config)
            model_trainer.train()
        except Exception as e:
            raise e
