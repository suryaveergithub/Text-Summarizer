import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
from documentTextExractor import PdfTextExtractor
import re
def add_full_stops(text):
    # Split the text into sentences
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s+', text)
    
    # Check if each sentence ends with a punctuation mark
    for i in range(len(sentences)):
        if not re.search(r'[.!?]$', sentences[i]):
            # Add a full stop at the end of the sentence
            sentences[i] += '.'
    
    # Join the sentences back together into a single string
    corrected_text = ' '.join(sentences)
    
    return corrected_text

def preprocess_text(text):
    # Tokenize the text into sentences and words
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    
    # Convert words to lowercase
    words = [word.lower() for word in words]
    
    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    words = [word for word in words if word not in stop_words]
    
    return sentences, words

def calculate_sentence_scores(sentences, word_scores):
    sentence_scores = {}
    for sentence in sentences:
        for word in nltk.word_tokenize(sentence.lower()):
            if word in word_scores.keys():
                if len(sentence.split(' ')) < 30:  # Consider only sentences less than 30 words
                    if sentence not in sentence_scores.keys():
                        sentence_scores[sentence] = word_scores[word]
                    else:
                        sentence_scores[sentence] += word_scores[word]
    
    return sentence_scores

def summarize_text(text, num_sentences=3):
    sentences, words = preprocess_text(text)
    
    # Calculate word frequencies
    word_freq = FreqDist(words)
    
    # Calculate word scores
    word_scores = {}
    for word in word_freq.keys():
        word_scores[word] = word_freq[word] / max(word_freq.values())
    
    # Calculate sentence scores
    sentence_scores = calculate_sentence_scores(sentences, word_scores)
    
    # Sort sentences by score in descending order
    sorted_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Select the top 'num_sentences' sentences for summary
    summary_sentences = [sentence for sentence, score in sorted_sentences[:num_sentences]]
    
    # Join the selected sentences to form the summary
    summary = ' '.join(summary_sentences)
    
    return summary


pdf_extractor = PdfTextExtractor("example.pdf")

# Call the extract_text method to extract text from the PDF
# extracted_text = pdf_extractor.extract_text()

text="""
Once upon a time in a quaint little town nestled between rolling hills and whispering forests, there lived two souls destined to find each other amidst the gentle whispers of fate.

Emma was a free-spirited artist, her canvas filled with the vibrant hues of life, and her heart painted with the dreams of wanderlust. She wandered through life with an insatiable curiosity, seeking inspiration in every corner of the world.

On the other side of town lived James, a reserved writer whose words danced with the rhythm of his heart. He found solace in the quiet corners of his study, where he could lose himself in the pages of his imagination.

Their paths first crossed one sunny afternoon in the town's bustling marketplace. Emma's laughter floated through the air like a melody, drawing James's attention from his thoughts. As their eyes met, something stirred within them—a spark of recognition that neither could ignore.

From that moment on, their lives became intertwined like the threads of destiny weaving a beautiful tapestry. They met in the park, under the shade of ancient trees, where they shared stories and dreams until the stars painted the sky with their shimmering light.

With each passing day, their connection grew stronger, like two magnets irresistibly drawn together. Emma's wild spirit ignited a fire in James's soul, while his quiet wisdom grounded her flights of fancy.

But love, like a delicate flower, is not immune to the storms of life. Doubts and fears crept into their hearts, threatening to tear them apart. Emma's wanderlust whispered of distant lands calling her name, while James's insecurities whispered of inadequacy and fear of losing her.

In the midst of their turmoil, they found refuge in each other's arms, where words were unnecessary, and love spoke in the language of the heart. Together, they learned that true love is not about holding on tightly but about setting each other free to chase their dreams.

In the end, they realized that love was not a destination but a journey—a journey they were willing to embark on together, hand in hand, wherever the winds of fate may lead.

And so, amidst the backdrop of their small town's enchanting beauty, Emma and James wrote their own love story—a story of two souls bound together by destiny, forever entwined in the embrace of love's timeless embrace.

"""
corrected_text = add_full_stops(text)



summary = summarize_text(corrected_text,4)
print("Summary:")
print(summary)