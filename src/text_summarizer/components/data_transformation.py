import pandas as pd
import os
from text_summarizer.entity import DataTransformationConfig
from text_summarizer.logging import logger
from transformers import AutoTokenizer
from datasets import DatasetDict, Dataset


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
        self.tokenizer = AutoTokenizer.from_pretrained(config.tokenizer_name)

    def convert_examples_to_features(self, example_batch):
        input_encodings = self.tokenizer(
            example_batch['dialogue'], max_length=1024, truncation=True)

        with self.tokenizer.as_target_tokenizer():
            target_encodings = self.tokenizer(
                example_batch['summary'], max_length=128, truncation=True)

        return {
            'input_ids': input_encodings['input_ids'],
            'attention_mask': input_encodings['attention_mask'],
            'labels': target_encodings['input_ids']
        }

    def split_dataset(self, df):
        # Chuyển đổi dữ liệu thành định dạng Dataset
        dataset_dict = DatasetDict()

        # Tách dữ liệu thành tập huấn luyện, tập kiểm tra và tập validation
        train_df = df.sample(frac=0.8, random_state=42)
        val_test_df = df.drop(train_df.index)
        val_df = val_test_df.sample(frac=0.5, random_state=42)
        test_df = val_test_df.drop(val_df.index)

        # Tạo Dataset cho mỗi tập
        train_dataset = Dataset.from_pandas(
            train_df.rename(columns={"Unnamed: 0": "id"}))
        val_dataset = Dataset.from_pandas(
            val_df.rename(columns={"Unnamed: 0": "id"}))
        test_dataset = Dataset.from_pandas(
            test_df.rename(columns={"Unnamed: 0": "id"}))

        # Gán features
        train_dataset = train_dataset.map(lambda example: {
                                          'id': example['id'], 'dialogue': example['Document'], 'summary': example['Summary']})
        val_dataset = val_dataset.map(lambda example: {
                                      'id': example['id'], 'dialogue': example['Document'], 'summary': example['Summary']})
        test_dataset = test_dataset.map(lambda example: {
                                        'id': example['id'], 'dialogue': example['Document'], 'summary': example['Summary']})

        # Đưa các dataset vào DatasetDict
        dataset_dict["train"] = train_dataset
        dataset_dict["validation"] = val_dataset
        dataset_dict["test"] = test_dataset

        return dataset_dict

    def convert(self):
        df = pd.read_csv(self.config.data_path)
        dataset_dict = self.split_dataset(df)
        dataset_samsum_pt = dataset_dict.map(
            self.convert_examples_to_features, batched=True)
        dataset_samsum_pt.save_to_disk(os.path.join(
            self.config.root_dir, "summarize_dataset"))
