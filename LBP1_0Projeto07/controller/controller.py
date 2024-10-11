from flask import Flask, Blueprint, render_template, request, url_for, redirect
from model.model import addPessoa, listaPessoas

blueprint_geral = Blueprint("blueprint_daora", __name__)