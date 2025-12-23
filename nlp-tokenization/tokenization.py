


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

    def __init__(self, tokenizer_method_name):
        self.model_name = tokenizer_method_name

    def add_text(self, text):
        self.text = text

    def get_unicode_code(self):
        return [ord(str) for str in self.text]
    
    def raw_bytes_to_integer(self):
        self.text_utf8 = self.text.encode('utf-8')

        text_integers_list = list(map(int, self.text_utf8))

        self.text_integers_list = text_integers_list

    def get_pairs(self):
        pair_dict = {}

        for pair in zip(self.text_integers_list, self.text_integers_list[1:]):
            pair_dict[pair] = pair_dict.get(pair, 0) + 1
            
        return pair_dict
        

    

# Initialize
tokenizer = tokenizerModel("Test Model")

tokenizer.add_text(sample_string)

bytes_to_int = tokenizer.raw_bytes_to_integer()

pairs = tokenizer.get_pairs()

#print(sorted([(count, pair) for pair, count in pairs.items()], reverse=True))
most_frequent_pair = max(pairs, key=pairs.get)

print("Most frequently occurring pair: ", most_frequent_pair)

def replace_common_pair(pair_list, most_frequent_pair, replace_id):
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

# BPE training
vocab_size = 276  # hyperparameter: the desired final vocabulary size
num_merges = vocab_size - 256
pairs = tokenizer.get_pairs()

for i in range(num_merges):
    # count up all the pairs
    stats = tokenizer.get_pairs()
    # find the pair with the highest count
    pair = max(stats, key=stats.get)
    # mint a new token: assign it the next available id
    idx = 256 + i
    # replace all occurrences of pair in tokens with idx
    pairs = replace_common_pair(pairs, pair, idx)
    # print progress
    print(f"merge {i+1}/{num_merges}: {pair} -> {idx} ({stats[pair]} occurrences)")

