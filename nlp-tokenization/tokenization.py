


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

print(tokenizer.get_pairs())
# top_pair = max(pair_dict, key=pair_dict.get)
# print(top_pair)
