from flask import Flask, request, render_template, redirect
from flask_jsglue import JSGlue 
import util
import difflib 

application = Flask(__name__)


jsglue = JSGlue() 
jsglue.init_app(application) 

util.load_artifacts() 


dishes, diet_of_dishes = util.get_dishes_name()
search_dishes = dishes 


@application.route("/")
def home():
    dishes, diet_of_dishes = util.get_dishes_name() 

   
    total_pages = round(len(dishes) / 28) + 1
    dishes= dishes[0: 28]
    diet_of_dishes = ["all_diet"] * 28

    
    final_dishes = dict(zip(dishes, diet_of_dishes))

    return render_template("home.html", dishes = final_dishes, total_pages = total_pages, current_page = 1, page_type = "main", nav_active_home = "active", search_dishes = search_dishes)
   
@application.route("/page/<int:pagenum>")
def page(pagenum):
    dishes, diet_of_dishes = util.get_dishes_name() 

    
    total_pages = round(len(dishes) / 28)
    reminder = len(dishes) % 28 
    if reminder != 0:
        total_pages += 1 

    dishes = dishes[28 * (pagenum - 1): 28 * pagenum] 
    diet_of_dishes = ["all_diet"] * len (dishes) 

    
    final_dishes = dict(zip(dishes, diet_of_dishes))

    return render_template("home.html", dishes = final_dishes, total_pages = total_pages, current_page = pagenum, page_type = "main" , nav_active_home = "active", search_dishes = search_dishes)
    

@application.route("/diet", defaults = {"name": "all", "pagenum": 1})
@application.route("/diet/<name>", defaults = {"pagenum": 1})
@application.route("/diet/<name>/<int:pagenum>") 
def diet(name, pagenum):
    dishes, diet_of_dishes = util.get_diet_wise_dishes(name)  
    total_pages = round(len(dishes) / 28)
    reminder = len(dishes) % 28
    if reminder != 0:
        total_pages += 1

    dishes = dishes[28 * (pagenum - 1): 28 * pagenum]

    
    if name == "vegetarian" or name == "non-vegetarian":
        diet_of_dishes = diet_of_dishes[28 * (pagenum - 1): 28 * pagenum]
    else:
        diet_of_dishes = ["all_diet"] * len(dishes)

    
    final_dishes = dict(zip(dishes, diet_of_dishes))

    return render_template("home.html", dishes=final_dishes, current_diet = name, total_pages = total_pages, current_page = pagenum, page_type = "diet", nav_active_home = "active", search_dishes = search_dishes)
    


@application.route("/state", defaults = {"name": "Gujarat", "diet": "all", "pagenum": 1})
@application.route("/state/<name>", defaults = {"diet": "all","pagenum": 1})
@application.route("/state/<name>/<diet>", defaults = {"pagenum": 1})
@application.route("/state/<name>/<diet>/<int:pagenum>") 
def state(name, diet, pagenum):
    state = util.get_state_name() 
    selected_state = name 
    dishes, diet_of_dishes = util.get_state_wise_dishes(name, diet) 

    
    total_pages = round(len(dishes) / 28)
    reminder = len(dishes) % 28
    if reminder != 0:
        total_pages+= 1

    dishes = dishes[28 * (pagenum - 1): 28 * pagenum]

    
    if diet == "vegetarian" or diet == "non-vegetarian":
        diet_of_dishes = diet_of_dishes[28 * (pagenum - 1): 28 * pagenum]
    else:
        diet_of_dishes = ["all_diet"] * len(dishes)

    
    final_dishes = dict(zip(dishes, diet_of_dishes))

    return render_template("state.html", state = state, selected_state = selected_state, dishes = final_dishes, current_diet = diet, total_pages = total_pages, current_page = pagenum, nav_active_state = "active", search_dishes = search_dishes)



@application.route("/region", defaults = {"name": "all regions", "diet": "all", "pagenum": 1})
@application.route("/region/<name>", defaults = {"diet": "all", "pagenum": 1})
@application.route("/region/<name>/<diet>", defaults = {"pagenum": 1})
@application.route("/region/<name>/<diet>/<int:pagenum>") 
def region(name, diet, pagenum):
    selected_region = name 
    dishes, diet_of_dishes = util.get_region_wise_dishes(name, diet) 

    
    total_pages = round(len(dishes) / 28)
    reminder = len(dishes) % 28
    if reminder != 0:
        total_pages += 1

    dishes = dishes[28 * (pagenum - 1): 28 * pagenum]

    
    if diet == "vegetarian" or diet == "non-vegetarian":
        diet_of_dishes = diet_of_dishes[28 * (pagenum - 1): 28 * pagenum]
    else:
        diet_of_dishes = ["all_diet"] * len(dishes)

    
    final_dishes = dict(zip(dishes, diet_of_dishes))

    return render_template("region.html", dishes = final_dishes, selected_region = selected_region, current_diet = diet, total_pages = total_pages, current_page = pagenum, nav_active_region = "active", search_dishes = search_dishes)
    


@application.route("/recipe", defaults = {"name": "all"})
@application.route("/recipe/<name>") 
def recipe(name):
    if name == "all": 
        return redirect("/")
    name = name.lower() 
    all_dishes = dishes 
    if name in all_dishes: 
        recommended_dishes = util.get_recommendation(name) 
        recipe_id = util.get_recipe(name) 

        return render_template("recipe.html", current_dish = name, recommended_dishes = recommended_dishes, recipe_id = recipe_id, search_dishes = search_dishes)
     

    return render_template("recipe.html") 


@application.route("/search", methods = ["GET"])
def search():
    if request.method == "GET": 
        search_query = request.args.get("searchquery") 
        search_result = difflib.get_close_matches(search_query.lower(), search_dishes)
        if len(search_result) > 0: 
            return render_template("search.html", dishes = search_result , search_dishes = search_dishes, current_search = search_query)
        else: 
            return render_template("search.html", dishes = search_result , search_dishes = search_dishes, current_search = search_query, no_record_found = True)
    else: 
        return redirect("/")


@application.errorhandler(404)
def page_not_found(e):
    
    return render_template("404.html", search_dishes = search_dishes), 404

if __name__ == "__main__":
    application.run()