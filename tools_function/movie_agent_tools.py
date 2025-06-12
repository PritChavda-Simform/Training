from utils_function.model_llm import llm 
from langchain_core.tools import tool
import requests
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

@tool
def movie_playlist(payload) -> str:
    """
        Generates a curated playlist of movies based on a specified genre. This tool takes in a genre (e.g., Action, Comedy, Drama,horror) and returns a list of movies that belong to that genre. It's useful when the user already knows the genre they are interested in and wants a themed movie list.
    """

    url = "https://movie-database-api1.p.rapidapi.com/list_movies.json"

    querystring = {"limit":"20","page":"1","quality":"all","genre":f"{payload}","minimum_rating":"0","query_term":"0","sort_by":"date_added","order_by":"desc","with_rt_ratings":"false"}

    headers = {
        "x-rapidapi-key": "e5d7d38636mshd52edaf9d5e78bbp1bdd7bjsn19c7e042613f",
        "x-rapidapi-host": "movie-database-api1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    result = response.json()
    movie_list= []
    for i in result['data']['movies']:
        movie_list.append(i['title'])
    return movie_list

@tool 
def movie_recommender(payload):

    """
        Recommends movies based on the user’s current mood. This tool analyzes the emotional tone provided by the user (e.g., feeling happy, sad, bored) and suggests movies that align with or help balance that mood. It's ideal for users who don't have a specific genre in mind but want a movie that matches how they feel.
    """
    url = f"https://tastedive.com/api/similar?q={payload}&type=movie&k=1050768-multiage-ED6F2DEB&info=1&limit=10"
    
    response = requests.get(url)
    result = response.json()
    movie_list = []
    for i in result['similar']['results']:
        movie_list.append(i['name'])
    print("movie names is this :", movie_list)
    return movie_list




@tool 
def movie_info(payload):
    """
        The function is summarize movies
    """

    promp = PromptTemplate(
        template=f"give me an information of {payload} movie",
        input_variables=['payload']
        )
    parser = StrOutputParser()
    chain = promp | llm | parser

    result = chain.invoke({'movie_name':f'{payload}'})
    return result
