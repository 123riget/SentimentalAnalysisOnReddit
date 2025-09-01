import os 
import matplotlib 
import seaborn as sns 
from wordcloud import WordCloud
import base64
from io import BytesIO 
from collections import Counter
import re 
matplotlib.use('Agg')
import matplotlib.pyplot as plt 


def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path) 
        
def generate_graphs(sentiment_results, topic):
    # extract sentiment labels and scores 
    sentiments = [result['sentiment'] for result in sentiment_results]
    scores = [result['score'] for result in sentiment_results]
    
    
    images_dir = os.path.join('static','images')
    create_directory(images_dir)
    
    bar_chart_path = os.path.join(images_dir, 'sentiment_bar_chart.png')
    word_chart_path = os.path.join(images_dir, 'word_cloud.png')
    
    # define bar plot 
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x = sentiments, y=scores, palette='coolwarm')
    plt.title("Sentiment scores for reddit post on {topic}", fontsize= 16)
    plt.xlabel("Sentiments", fontsize=12)
    plt.ylabel("Scores", fontsize = 12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}',
                    (p.get_x() + p.get_width()/2., p.get_height()), 
                    ha = 'center', va = 'center',fontsize=12, color = 'black',
                    xytext = (0, 5), textcoords = 'offset points')
    plt.grid(True, linestyle = '--', alpha = 0.7)
    plt.savefig(bar_chart_path)
    plt.close() 
        
    # converting bar chart into base64 to return in the api response
    bar_img_b64 = encode_image_to_base64(bar_chart_path)
    # generating world cloud for most frequent word 
    text = ' '.join([result['content'] for result in sentiment_results])
    
    # clean the text removing spl characters, number 
    text = re.sub(r'[^A-Za-z\s]','', text.lower())
    
    # tokenize
    words = text.split()
    word_counts = Counter(words)
    
    # generate the word cloud 
    wordcloud = WordCloud(width = 800, height = 400, background_color = 'white', max_words = 200, colormap = 'viridis').generate_from_frequencies(word_counts)
    # save word cloud as png file 
    
    wordcloud.to_file(word_chart_path)
    
    # convert the word cloud img to base64 
    word_cloud_b64 = encode_image_to_base64(word_chart_path)
    return bar_img_b64, word_cloud_b64

def encode_image_to_base64(image_path):
    with open(image_path, 'rb') as img_file:
        img_64 = base64.b64encode(img_file.read()).decode('utf-8')
    return img_64
    
