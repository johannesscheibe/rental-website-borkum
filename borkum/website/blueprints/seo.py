from flask import Blueprint, render_template, Response, url_for, current_app, request
from datetime import datetime
import json
import os

seo = Blueprint('seo', __name__)

@seo.route('/sitemap.xml')
def sitemap():
    """Generate sitemap.xml dynamically"""
    base_url = request.url_root.rstrip('/')
    if base_url.startswith('http://'):
        base_url = base_url.replace('http://', 'https://')
    
    # Get all apartment pages
    res_path = current_app.config['STORAGE_PATH']
    apartments_json = os.path.join(res_path, 'content', 'apartments.json')
    apartments = []
    if os.path.exists(apartments_json):
        with open(apartments_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
            apartments = list(data.keys())
    
    # Priority and changefreq for different page types
    pages = [
        {'url': '/', 'priority': '1.0', 'changefreq': 'weekly'},
        {'url': '/gallery', 'priority': '0.8', 'changefreq': 'monthly'},
        {'url': '/location', 'priority': '0.7', 'changefreq': 'monthly'},
        {'url': '/impressum', 'priority': '0.3', 'changefreq': 'yearly'},
        {'url': '/privacy', 'priority': '0.3', 'changefreq': 'yearly'},
        {'url': '/terms_of_use', 'priority': '0.3', 'changefreq': 'yearly'},
    ]
    
    # Add apartment pages
    for apt in apartments:
        pages.append({
            'url': f'/apartment/{apt}',
            'priority': '0.9',
            'changefreq': 'monthly'
        })
    
    # Generate XML
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    for page in pages:
        xml.append('  <url>')
        xml.append(f'    <loc>{base_url}{page["url"]}</loc>')
        xml.append(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>')
        xml.append(f'    <changefreq>{page["changefreq"]}</changefreq>')
        xml.append(f'    <priority>{page["priority"]}</priority>')
        xml.append('  </url>')
    
    xml.append('</urlset>')
    
    return Response('\n'.join(xml), mimetype='application/xml')


@seo.route('/robots.txt')
def robots():
    """Generate robots.txt"""
    base_url = request.url_root.rstrip('/')
    sitemap_url = f"{base_url}/sitemap.xml"
    
    robots_content = f"""User-agent: *
Allow: /

Sitemap: {sitemap_url}
"""
    
    return Response(robots_content, mimetype='text/plain')

