from transformers import AutoTokenizer, AutoModel
import torch
from torch.nn import functional
import os
# Initialize tokenizer and model
tokenizer = AutoTokenizer.from_pretrained('deepset/sentence_bert')
model = AutoModel.from_pretrained('deepset/sentence_bert')
# Define your labels for the classification
labels = ['Indicative of a Bank Run', 'Not indicative of a Bank Run']
directory = './files/filtered_json_files'
output_directory = './files/predicted_json_files_sbert'
# Ensure output directory exists
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        output_data = []
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    # Find the 'body' field in the JSON line
                    body_header = line.find('"body": "')
                    if body_header != -1:
                        # Extract the content of the 'body' field
                        body_text_start = body_header + 9
                        body_text_end = line.find('"', body_text_start)
                        tweet = line[body_text_start:body_text_end]
                        # Prepare tweet for model input
                        inputs = tokenizer.batch_encode_plus([tweet] + labels,
                                                             return_tensors='pt',
                                                             truncation = True,
                                                             pad_to_max_length=True)
                        input_ids = inputs['input_ids']
                        attention_mask = inputs['attention_mask']
                        with torch.no_grad():
                            output = model(input_ids, attention_mask=attention_mask)[0]
                        tweet_rep = output[:1].mean(dim=1)
                        label_reps = output[1:].mean(dim=1)
                        # Find the label with the highest cosine similarity to the tweet
                        similarities = functional.cosine_similarity(tweet_rep, label_reps)
                        closest_index = similarities.argmax()
                        predicted_label = labels[closest_index]
                        similarity_score = similarities[closest_index].item()
                        # Find the last closing brace to insert the prediction and similarity
                        last_brace = line.rfind('}')
                        if last_brace != -1:
                            # Insert the prediction and similarity before the last brace
                            insert_text = f', "predicted_label": "{predicted_label}", "similarity": {similarity_score}'
                            new_line = line[:last_brace] + insert_text + line[last_brace:]
                            output_data.append(new_line.strip())
                except Exception as e:
                    print(f"Error processing line in file {filename}: {e}")
        # Write data with predictions to a new file in the output directory
        if output_data:
            with open(os.path.join(output_directory, filename), 'w', encoding='utf-8') as outfile:
                for item in output_data:
                    outfile.write(item + '\n')