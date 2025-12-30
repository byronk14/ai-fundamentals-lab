import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


sample_string = """When Mr. Bilbo Baggins of Bag End announced that he would shortly be
celebrating his eleventy-first birthday with a party of special
magnificence, there was much talk and excitement in Hobbiton.
Bilbo was very rich and very peculiar, and had been the
wonder of the Shire for sixty years, ever since his remarkable
disappearance and unexpected return. The riches he had brought back
from his travels had now become a local legend, and it was popularly
believed, whatever the old folk might say, that the Hill at Bag End
was full of tunnels stuffed with treasure. And if that was not enough
for fame, there was also his prolonged vigour to marvel at. Time wore
on, but it seemed to have little effect on Mr. Baggins. At ninety he
was much the same as at fifty. At ninety-nine they began to call him
well-preserved; but unchanged would have been nearer the mark. There
were some that shook their heads and thought this was too much of a
good thing; it seemed unfair that anyone should possess (apparently)
perpetual youth as well as (reputedly) inexhaustible wealth.
"It will have to be paid for," they said. "It isn"t natural,
and trouble will come of it!"""

class tokenizerModel:
    """ Class to handle testing of tokenizer """

    def __init__(self, tokenizer_method_name: str):
        self.model_name: str = tokenizer_method_name
        self.text: str = ''
        self.text_utf8: str = ''
        self.text_integers_list: list = []
        self.final_integers_list: list = []
        self.vocab_size: int = 276 #hyperparameter for desired final vocabulary size
        self.merged_pairs: dict = {}

    def add_text(self, text):
        self.text = text

    def get_unicode_code(self) -> list:
        return [ord(str) for str in self.text]
    
    def raw_bytes_to_integer(self) -> None:
        self.text_utf8 = self.text.encode('utf-8')

        text_integers_list = list(map(int, self.text_utf8))

        self.text_integers_list = text_integers_list
    
    def _replace_common_pair(self, pair_list: list, most_frequent_pair: tuple, replace_id: int) -> list:
        new_pair_list = []
        i = 0
        while i < len(pair_list):
            if pair_list[i] == most_frequent_pair[0] and pair_list[i + 1] == most_frequent_pair[1]:
                new_pair_list.append(replace_id)
                i += 2 
            else:
                new_pair_list.append(pair_list[i])
                i += 1

        return new_pair_list

    def get_pairs(self, text_integers_list: list) -> dict:
        pair_dict = {}

        for pair in zip(text_integers_list, text_integers_list[1:]):
            pair_dict[pair] = pair_dict.get(pair, 0) + 1
            
        return pair_dict
    
    def byte_pair_encode(self):
        # BPE training
        num_merges = self.vocab_size - 256

        text_integers_list = list(self.text_integers_list)
        merged_pairs = {}
        for i in range(num_merges):
            # count up all the pairs
            pairs = self.get_pairs(text_integers_list)
            # find the pair with the highest count
            pair = max(pairs, key=pairs.get)
            # mint a new token: assign it the next available id
            idx = 256 + i
            #print(f"merging {pair} into a new token {idx}")
            # replace all occurrences of pair in tokens with idx
            text_integers_list = self._replace_common_pair(text_integers_list, pair, idx)

            merged_pairs[pair] = idx
        
        self.merged_pairs = merged_pairs
        self.final_integers_list = text_integers_list

        logging.info(f"tokens length: {len(self.text_integers_list)}")
        logging.info(f"ids length: {len(text_integers_list)}")
        logging.info(f"compression ratio: {len(self.text_integers_list) / len(text_integers_list):.2f}X")

    def decode(self) -> str:
        if len(self.merged_pairs) == 0:
            raise "Run Byte pair encoding first before decoding"
        
        vocab = {idx: bytes([idx]) for idx in range(256)}

        for (p0, p1), idx in self.merged_pairs.items():
            vocab[idx] = vocab[p0] + vocab[p1]

        # given ids (list of integers), return Python string
        tokens = b"".join(vocab[idx] for idx in self.final_integers_list)
        text = tokens.decode("utf-8", errors="replace")

        return text
    
    def encode(self, text):
        # given a string, return list of integers (the tokens)
        tokens = list(text.encode("utf-8"))

        while len(tokens) >= 2:
            stats = self.get_pairs(tokens)
            pair = min(stats, key=lambda p: self.merged_pairs.get(p, float("inf")))
            if pair not in self.merged_pairs:
                break # nothing else can be merged
            idx = self.merged_pairs[pair]
            tokens = self._replace_common_pair(tokens, pair, idx)

        return tokens


        

    

# Initialize
tokenizer = tokenizerModel("Test Model")

logging.info(f"Initilizing tokenizer -- model name: {tokenizer.model_name}")
logging.info(f"Initilizing tokenizer -- text: {tokenizer.text}")
logging.info(f"Initilizing tokenizer -- text utf8: {tokenizer.text_utf8}")
logging.info(f"Initilizing tokenizer -- text integer list: {tokenizer.text_integers_list}")

# Add sample string
tokenizer.add_text(sample_string)

# Convert sample string to list of UTF8 byte integers
bytes_to_int = tokenizer.raw_bytes_to_integer()

# Run byte pair encoding algorithm
tokenizer.byte_pair_encode()

# Run decoding function
tokenizer.decode()

# Run encoding function
print(tokenizer.encode("test string"))






