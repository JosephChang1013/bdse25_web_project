import random as rd
import pandas as pd
from ast import literal_eval

def users_recommendation(userId):
    df_user_recs=pd.read_csv('rating_userId_segment.csv').sort_values(by=['userId'])
    recs = df_user_recs[df_user_recs['userId']==userId]
    movieid = pd.Series(recs.iloc[0,1][1:-1].split(', '))
    rating = pd.Series(recs.iloc[0,2][1:-1].split(', '))
    rec_matrix = pd.DataFrame(movieid, columns = ["movieId"])
    rec_matrix["rating"] = rating
    return rec_matrix
def predict():
    # load df which recommend 30 movies for each user
    df_user_recs=pd.read_csv('rating_userId_segment.csv',index_col=[0]).sort_values(by=['userId'])
    files_movies=pd.read_csv('lates_movie_html.csv',index_col=[0])
    # random userId 
    user=rd.randint(0,len(df_user_recs))
    userId=users_recommendation(user)
    # users_cluser_recommendation(userId)
    userId['movieId']=userId['movieId'].astype(int)
    result_dict1=userId.merge(files_movies,on='movieId',how='inner').to_dict()
    # df to dict (JSON method(orient = 'records'))
    data= [{key: result_dict1[key][value] for key in [key for key in result_dict1]} for value in range(len(result_dict1["movieId"]))]
    # cluster recommender
    df112=pd.read_csv('rating_userId_segment.csv',converters={'movieId':literal_eval})
    seg = df112[df112.Segment.eq(df112[df112.userId.eq(user)].Segment.tolist()[0])]
    flat_list = [j for i in seg.movieId for j in i]
    cluster = list(set(flat_list))
    movie_to_user = seg[seg.userId.eq(user)].movieId.to_list()[0]
    movid_seg=pd.DataFrame(list(set(cluster).symmetric_difference(movie_to_user)), columns = ['movieId'])
    files_movies=pd.read_csv('lates_movie_html.csv',index_col=[0])
    result_dict2=movid_seg.merge(files_movies,on='movieId',how='inner').sort_values(by='count',ascending=False)[0:50].reset_index().to_dict()
    data2 = [{key: result_dict2[key][value] for key in [key for key in result_dict2]} for value in range(len(result_dict2["movieId"]))]
    return data,data2