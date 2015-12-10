# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

from gluon import utils as gluon_utils
import json


# @banana
def index():
    draft_id = gluon_utils.web2py_uuid()
    """Fetch the Game of the Year Category as the default active Category"""
    rows = db(db.cats.cat_name == "Game of the Year").select(db.cats.ALL)
    first_cat = rows.first()
    active_cat_id = first_cat.cat_id
    active_cat_name = first_cat.cat_name
    return dict(draft_id=draft_id, active_cat_id=active_cat_id, active_cat_name=active_cat_name)

def catsList():
    draft_id = gluon_utils.web2py_uuid()
    user_id = auth.user_id
    return dict(draft_id=draft_id, user_id=user_id)

def show_cat():
    draft_id = gluon_utils.web2py_uuid()
    cat_id = request.args(0)
    rows = db(db.cats.cat_id == cat_id).select(db.cats.ALL)
    first_cat = rows.first()
    cat_name = first_cat.cat_name
    user_id = auth.user_id
    response.flash = T(cat_name)
    return dict(draft_id=draft_id, cat_name=cat_name, cat_id=cat_id, user_id=user_id)

def show_comments():
    draft_id = gluon_utils.web2py_uuid()
    disc_id = request.args(0)
    user_id = auth.user_id
    rows = db(db.discs.disc_id == disc_id).select(db.discs.ALL)
    first_disc = rows.first()
    disc_name = first_disc.disc_name
    return dict(draft_id=draft_id, disc_name=disc_name, disc_id=disc_id, user_id=user_id)

def load_cats():
    """Loads all Categories"""
    rows = db().select(db.cats.ALL)
    number_of_votes = 0
    for v in rows:
        """fetches all games that match current category"""
        votes = db(db.games.cat_loc == v.cat_id).select(db.games.ALL)
        for vo in votes:
            number_of_votes += vo.game_votes
        db.cats.update_or_insert((db.cats.cat_id == v.cat_id),
            total_votes=number_of_votes)
        number_of_votes = 0
    """determines total number of discussions"""
    for di in rows:
        discs = db(db.discs.cat_loc == di.cat_id).count()
        db.cats.update_or_insert((db.cats.cat_id == di.cat_id),
            total_discs=discs)
    """determines front runner for each category"""
    for fr in rows:
        if db(db.games.cat_loc == fr.cat_id).count() > 0:
            fronter = 0
            fronter_name = "none"
            games = db(db.games.cat_loc == fr.cat_id).select(db.games.ALL)
            for g in games:
                if fronter < g.game_votes:
                    fronter = g.game_votes
                    fronter_name = g.game_name
            db.cats.update_or_insert((db.cats.cat_id == fr.cat_id),
                front_runner=fronter_name,
                front_votes=fronter)
    """loads the updated categories"""
    d = {r.cat_id: {'cat_name': r.cat_name,
                        'is_editing': r.is_editing,
                        'total_votes': r.total_votes,
                        'total_discs': r.total_discs,
                        'front_runner': r.front_runner,
                        'front_votes': r.front_votes,
                        }
         for r in rows}
    return response.json(dict(cat_dict=d))


def load_4_cats():
    """Loads the top 4 Categories"""
    rows = db().select(db.cats.ALL, limitby=(0,4))
    number_of_votes = 0
    for v in rows:
        """fetches all games that match current category"""
        votes = db(db.games.cat_loc == v.cat_id).select(db.games.ALL)
        for vo in votes:
            number_of_votes += vo.game_votes
        db.cats.update_or_insert((db.cats.cat_id == v.cat_id),
            total_votes=number_of_votes)
        number_of_votes = 0
    """determines total number of discussions"""
    for di in rows:
        discs = db(db.discs.cat_loc == di.cat_id).count()
        db.cats.update_or_insert((db.cats.cat_id == di.cat_id),
            total_discs=discs)
    """determines front runner for each category"""
    for fr in rows:
        if db(db.games.cat_loc == fr.cat_id).count() > 0:
            fronter = 0
            fronter_name = "none"
            games = db(db.games.cat_loc == fr.cat_id).select(db.games.ALL)
            for g in games:
                if fronter < g.game_votes:
                    fronter = g.game_votes
                    fronter_name = g.game_name
            db.cats.update_or_insert((db.cats.cat_id == fr.cat_id),
                front_runner=fronter_name,
                front_votes=fronter)
    """loads the updated categories"""
    d = {r.cat_id: {'cat_name': r.cat_name,
                        'is_editing': r.is_editing,
                        'total_votes': r.total_votes,
                        'total_discs': r.total_discs,
                        'front_runner': r.front_runner,
                        'front_votes': r.front_votes,
                        }
         for r in rows}
    return response.json(dict(cat_dict=d))

def load_discs():
    """Loads the correct discs within each cat"""
    discs_list = db(db.discs.cat_loc == request.vars.cat_id).select(db.discs.ALL)
    for com in discs_list:
        comments = db(db.comments.disc_loc == com.disc_id).count()
        db.discs.update_or_insert((db.discs.disc_id == com.disc_id),
            total_comments=comments)
    d = {r.disc_id: {'disc_name': r.disc_name,
                        'is_editing': r.is_editing,
                        'cat_loc': r.cat_loc,
                        'author': r.author,
                        'likes': r.likes,
                        'dislikes': r.dislikes,
                        'total_comments': r.total_comments,
                        }
         for r in discs_list}
    response.flash = T("Discs Loaded")
    return response.json(dict(disc_dict=d))

def load_games():
    """Loads the correct discs within each cat"""
    games_list = db(db.games.cat_loc == request.vars.cat_id).select(db.games.ALL)
    d = {r.game_id: {'game_name': r.game_name,
                        'is_editing': r.is_editing,
                        'cat_loc': r.cat_loc,
                        'author': r.author,
                        'game_votes': r.game_votes,
                        }
         for r in games_list}
    response.flash = T("Games Loaded")
    return response.json(dict(game_dict=d))

def load_comments():
    """Loads the correct comments within every disc"""
    coms_list = db(db.comments.disc_loc == request.vars.disc_id).select(db.comments.ALL)
    d = {r.com_id: {'com_name': r.com_name,
                        'is_editing': r.is_editing,
                        'disc_loc': r.disc_loc,
                        'author': r.author,
                        }
         for r in coms_list}
    response.flash = T("Comments Loaded")
    return response.json(dict(com_dict=d))

@auth.requires_signature()
def add_cat():
    db.cats.update_or_insert((db.cats.cat_id == request.vars.cat_id),
            author=request.vars.user_id,
            cat_id=request.vars.cat_id,
            cat_name=request.vars.cat,
            is_editing=request.vars.is_editing)
    return "ok"

@auth.requires_signature()
def add_disc():
    db.discs.update_or_insert((db.discs.disc_id == request.vars.disc_id),
            author=request.vars.user_id,
            disc_id=request.vars.disc_id,
            disc_name=request.vars.disc,
            cat_loc=request.vars.cat_loc,
            is_editing=request.vars.is_editing)
    response.flash = T("Disc Created")
    return "ok"

@auth.requires_signature()
def add_game():
    db.games.update_or_insert((db.games.game_id == request.vars.game_id),
            author=request.vars.user_id,
            game_id=request.vars.game_id,
            game_name=request.vars.game,
            cat_loc=request.vars.cat_loc,
            is_editing=request.vars.is_editing)
    return "ok"

@auth.requires_signature()
def add_comment():
    db.comments.update_or_insert((db.comments.com_id == request.vars.com_id),
            author=request.vars.user_id,
            com_id=request.vars.com_id,
            com_name=request.vars.com,
            disc_loc=request.vars.disc_loc,
            is_editing=request.vars.is_editing)
    return "ok"

@auth.requires_signature()
def edit_cat():
    db.cats.update_or_insert((db.cats.cat_id == request.vars.cat_id),
            is_editing=request.vars.is_editing)
    return "ok"

@auth.requires_signature()
def edit_disc():
    db.discs.update_or_insert((db.discs.disc_id == request.vars.disc_id),
            is_editing=request.vars.is_editing)
    return "ok"

@auth.requires_signature()
def edit_game():
    db.games.update_or_insert((db.games.game_id == request.vars.game_id),
            is_editing=request.vars.is_editing)
    return "ok"

def cast_vote():
    db.games.update_or_insert((db.games.game_id == request.vars.game_id),
            game_votes=request.vars.votes)
    return "ok"

def cast_like():
    db.discs.update_or_insert((db.discs.disc_id == request.vars.disc_id),
            likes=request.vars.the_likes)
    return "ok"

def cast_dislike():
    db.discs.update_or_insert((db.discs.disc_id == request.vars.disc_id),
            dislikes=request.vars.the_dislikes)
    return "ok"

@auth.requires_signature()
def delete_cat():
    cat_to_delete = request.vars.cat_id
    """delete the selected Category"""
    db(db.cats.cat_id == cat_to_delete).delete()
    db(db.discs.cat_loc == cat_to_delete).delete()
    return "ok"

@auth.requires_signature()
def delete_disc():
    disc_to_delete = request.vars.disc_id
    """delete the selected Discussion"""
    db(db.discs.disc_id == disc_to_delete).delete()
    db(db.comments.disc_loc == disc_to_delete).delete()
    return "ok"

@auth.requires_signature()
def delete_game():
    game_to_delete = request.vars.game_id
    """delete the selected Game"""
    db(db.games.game_id == game_to_delete).delete()
    return "ok"

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


