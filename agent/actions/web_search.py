import requests
from urllib.parse import quote
from typing import List, Dict

def web_search(query: str, num_results: int = 5) -> str:
    """
    Recherche sur le web en utilisant l'API DuckDuckGo Instant Answer.
    
    Args:
        query: La requête de recherche
        num_results: Nombre de résultats à retourner (par défaut 5)
    
    Returns:
        str: Résultats de recherche formatés
    """
    try:
        # Utiliser l'API DuckDuckGo Instant Answer
        url = "https://api.duckduckgo.com/"
        params = {
            "q": query,
            "format": "json",
            "no_html": 1,
            "skip_disambig": 1
        }
        
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        results = []
        
        # Récupérer l'abstract (résumé principal)
        if data.get("Abstract"):
            results.append(f"📌 Résumé: {data['Abstract']}")
            if data.get("AbstractURL"):
                results.append(f"🔗 Source: {data['AbstractURL']}")
        
        # Récupérer les topics relatés
        if data.get("RelatedTopics"):
            results.append("\n🔍 Résultats connexes:")
            count = 0
            for topic in data["RelatedTopics"]:
                if count >= num_results:
                    break
                if isinstance(topic, dict) and "Text" in topic:
                    results.append(f"\n• {topic['Text']}")
                    if topic.get("FirstURL"):
                        results.append(f"  🔗 {topic['FirstURL']}")
                    count += 1
        
        if not results:
            # Fallback: recherche HTML parsing (simple)
            search_url = f"https://html.duckduckgo.com/html/?q={quote(query)}"
            results.append(f"🔍 Recherche effectuée pour: '{query}'")
            results.append(f"🌐 Voir les résultats complets: {search_url}")
        
        result_text = "\n".join(results)
        print(f"✅ Recherche web effectuée: {query}")
        print(result_text)
        
        return result_text
        
    except requests.exceptions.RequestException as e:
        error_msg = f"❌ Erreur lors de la recherche web: {str(e)}"
        print(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"❌ Erreur inattendue: {str(e)}"
        print(error_msg)
        return error_msg

# Made with Bob
