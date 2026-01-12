import string
import random
from datetime import datetime, timedelta, timezone
from flask import Blueprint, render_template, request, redirect, abort
from .models import Link, db

bp = Blueprint('main', __name__)

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

def ensure_utc(dt):
    """Garante que a data tenha timezone UTC se vier 'naive' do banco."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt

@bp.route('/', methods=['GET', 'POST'])
def home():
    short_url = None
    if request.method == 'POST':
        original_url = request.form['url']
        
        existing_link = Link.query.filter_by(original_url=original_url).first()
        
        if existing_link:
            # CORREÇÃO: Usar a função auxiliar para garantir UTC
            created_at = ensure_utc(existing_link.created_at)
            expiration_time = created_at + timedelta(hours=24)
            
            if datetime.now(timezone.utc) > expiration_time:
                db.session.delete(existing_link)
                db.session.commit()
                existing_link = None
        
        if existing_link:
            code = existing_link.short_code
        else:
            code = generate_short_code()
            while Link.query.filter_by(short_code=code).first():
                code = generate_short_code()
            
            new_link = Link(original_url=original_url, short_code=code)
            db.session.add(new_link)
            db.session.commit()
        
        short_url = request.host_url + code
        
    return render_template('index.html', short_url=short_url)

@bp.route('/<short_code>')
def redirect_to_url(short_code):
    link = Link.query.filter_by(short_code=short_code).first()
    
    if link:
        # CORREÇÃO: O SQLite retorna a data sem fuso (naive).
        # Adicionamos o fuso UTC manualmente antes de comparar.
        created_at = ensure_utc(link.created_at)
        expiration_time = created_at + timedelta(hours=24)
        
        # Agora ambos os lados são "offset-aware" (conscientes do fuso)
        if datetime.now(timezone.utc) > expiration_time:
            db.session.delete(link)
            db.session.commit()
            return abort(404)
            
        return redirect(link.original_url)
    else:
        return abort(404)