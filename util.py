import pandas as pd
import pickle
import sklearn


data = None
model = None
model_data_frame = None


def load_artifacts():
    global data, model, model_data_frame 
    data = pd.read_csv("artifacts/cleaned_data.csv") 
    model_data_frame = pd.read_csv("artifacts/model_data.csv", index_col="name") 
    with open("artifacts/model.pickle", "rb") as f:
        model = pickle.load(f) 


def get_dishes_name():
    global data 
    dishes_name = data.name.to_list() 
    diet_of_dishes = data.diet.to_list()  
    return dishes_name, diet_of_dishes  


def get_diet_wise_dishes(diet):
    global data 

    if diet == "vegetarian":
        df = data.loc[data.diet == diet, ["name", "diet"]] 
        return df.name, df.diet
    elif diet == "non-vegetarian":
        df = data.loc[data.diet == diet, ["name", "diet"]] 
        return df.name, df.diet
    else:
        return get_dishes_name() 


def get_state_name():
    global data 
    return list(data.state.unique()) 


def get_state_wise_dishes(state, diet):
    global data 
    verify_state = state in data.state.to_list() 
    if diet == "vegetarian" or diet == "non-vegetarian": 
        if verify_state: 
            if state == "All State": 
                return get_diet_wise_dishes(diet)
            else: 
                df = data.loc[(data.state == state) & (data.diet == diet), ["name", "diet"]]
                return df.name, df.diet 
        else: 
            return get_diet_wise_dishes(diet)
    else: 
        if verify_state: 
            if state == "All State":
                return get_dishes_name()
            else:
                df = data.loc[data.state == state,["name", "diet"]]
                return df.name, df.diet
        else:
            return get_dishes_name()


def get_region_wise_dishes(region, diet):
    global data 
    verify_region = region.title() in data.region.to_list()
    if diet == "vegetarian" or diet == "non-vegetarian": 
        if verify_region: 
            df = data.loc[(data.region == region.title()) & (data.diet == diet), ["name", "diet"]]
            return df.name, df.diet
        else:
            return get_diet_wise_dishes(diet)
    else:
        if verify_region:
            df = data.loc[data.region == region.title(), ["name", "diet"]]
            return df.name, df.diet
        else:
            return get_dishes_name()


def get_recipe(dish):
    global data 
    return data.loc[data.name == dish, ["recipe"]].values[0][0]


def get_recommendation(dish):
    global model, model_data_frame 

    X = model_data_frame[model_data_frame.index == dish] 
    distance, cuisine_index = model.kneighbors(X, n_neighbors = 13)  

    recommendation_result = []
    for c in cuisine_index.flatten(): 
        recommended_dish = model_data_frame.index[c] 
        if recommended_dish == dish: 
            continue
        recommendation_result.append(recommended_dish) 
    return recommendation_result[:12] 
