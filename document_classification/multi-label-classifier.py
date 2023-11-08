from torch import nn
from transformers import AutoModel, AutoTokenizer


class MultiLabelClassifier(nn.Module):
    def __init__(self, bert_model, number_of_labels):
        super(MultiLabelClassifier, self).__init__()
        self.text_encoder = AutoModel.from_pretrained(bert_model)
        for param in self.text_encoder.parameters():
            param.requires_grad = False

        input_size = 768
        self.post_layers = nn.Sequential(
                nn.Linear(input_size, number_of_labels),
                nn.Sigmoid())

    def forward(self, tokens):
        tokens.to(self.text_encoder.device)
        x = self.text_encoder(**tokens)
        if self.pooling_strategy == 'cls':
            bert_output = x['last_hidden_state'][:, 0, :]
        elif self.pooling_strategy == 'pool':
            bert_output = x['pooler_output']

        x = self.post_layers(bert_output)
        return x