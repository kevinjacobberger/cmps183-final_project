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
    rows = db(db.cats.cat_name == "Monkeys").select(db.cats.ALL)
    first_cat = rows.first()
    active_cat_id = first_cat.cat_id
    active_cat_name = first_cat.cat_name
    return dict(draft_id=draft_id, active_cat_id=active_cat_id, active_cat_name=active_cat_name)

def catsList():
    draft_id = gluon_utils.web2py_uuid()
    user_id = auth.user_id
    return dict(draft_id=draft_id, user_id=user_id)

def show_cat():
    query = (db.votes.author==auth.user_id) & (db.votes.cat_loc==request.args(0))
    rows = db(query).select(db.votes.ALL)
    user_vote = rows.first()
    has_voted = False;
    if user_vote is None:
        session.flash = T("votes None")
        has_voted = False
    else:
        session.flash = T("votes not None")
        has_voted = user_vote.has_voted
    draft_id = gluon_utils.web2py_uuid()
    cat_id = request.args(0)
    rows = db(db.cats.cat_id == cat_id).select(db.cats.ALL)
    first_cat = rows.first()
    cat_name = first_cat.cat_name
    user_id = auth.user_id
    has_voted = json.dumps(has_voted)
    return dict(draft_id=draft_id, cat_name=cat_name, cat_id=cat_id, user_id=user_id,has_voted=has_voted)

def load_cats():
    """Loads all Categories"""
    rows = db().select(db.cats.ALL)
    d = {r.cat_id: {'cat_name': r.cat_name,
                        'is_editing': r.is_editing,
                        }
         for r in rows}
    return response.json(dict(cat_dict=d))

def load_discs():
    """Loads the correct discs within each cat"""
    discs_list = db(db.discs.cat_loc == request.vars.cat_id).select(db.discs.ALL)
    d = {r.disc_id: {'disc_name': r.disc_name,
                        'is_editing': r.is_editing,
                        'cat_loc': r.cat_loc,
                        'author': r.author,
                        'likes': r.likes,
                        'dislikes': r.dislikes,
                        }
         for r in discs_list}
    return response.json(dict(disc_dict=d))

def load_games():
    """Loads the correct discs within each cat"""
    games_list = db(db.games.cat_loc == request.vars.cat_id).select(db.games.ALL)
    d = {r.game_id: {'game_name': r.game_name,
                        'game_id':r.game_id,
                        'is_editing': r.is_editing,
                        'cat_loc': r.cat_loc,
                        'author': r.author,
                        'game_votes': r.game_votes,
                        }
         for r in games_list}
    return response.json(dict(game_dict=d))

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
            game_votes=0,
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
    db.votes.update_or_insert((db.votes.author==auth.user_id) &
            (db.votes.cat_loc==request.vars.cat_loc),
            cat_loc=request.vars.cat_loc,
            game_id=request.vars.game_id,
            has_voted=True)
    return "ok"

@auth.requires_signature()
def delete_cat():
    cat_to_delete = request.vars.cat_id
    """delete the selected Category"""
    db(db.cats.cat_id == cat_to_delete).delete()
    return "ok"

@auth.requires_signature()
def delete_disc():
    disc_to_delete = request.vars.disc_id
    """delete the selected Discussion"""
    db(db.discs.disc_id == disc_to_delete).delete()
    return "ok"

@auth.requires_signature()
def delete_game():
    game_to_delete = request.vars.game_id
    """delete the selected Game"""
    db(db.games.game_id == game_to_delete).delete()
    return "ok"



def reset():
    db(db.votes.id > 0).delete()
    session.flash = T("Database has been reset")
    redirect(URL('default', 'index'))
    return

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


