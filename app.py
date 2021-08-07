from flask import Flask, render_template, request
from nltk import pos_tag, RegexpParser
import nltk

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
	return render_template('index.html')

@app.route("/", methods=['POST'])
def endpoint():
	input_text = request.form.get('sentence')
	text = input_text.split()
	tokens_tag = pos_tag(text)
	"""
	NP: Single noun/noun phrase
		Determiner (the, a, an) or possessive pronoun followed by
		any number of adjectives then the noun
	CNP: Compound noun phrase, e.g. "A book about the emancipation of women"
									 N    P       N                       P
		 Separated by prepositions
	VP: Verb phrases composed of auxiliary verbs and/or a series of verbs
	"""
	grammar = """
	NP:{((<DT><VB.?>?)|<PRP\\$>)*<JJ.?>*<NN.?>*}
	CNP:{<NP>((<VB.?|IN>)<NP>)+}
	VP:{<MD>?<VB.?>+}
	"""
	chunker = RegexpParser(grammar)
	chunked = chunker.parse(tokens_tag)
	return render_template('index.html', tree_pos=chunked.pos())

if __name__ == "__main__":
	app.run(debug=True, port=5000)
