from flask import Flask, Blueprint, render_template, request, url_for, redirect
from model.model import addPessoa, listaPessoas

blueprint_default = Blueprint("blueprint_cool", __name__)
