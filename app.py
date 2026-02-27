from flask import Flask, render_template, request, jsonify
import requests
import time

app = Flask(__name__)

API_KEY = "3"

# Links das imagens dos times (mantendo seus links)
TEAM_BADGES = {
    "América-MG": "https://logodetimes.com/wp-content/uploads/america-mineiro.png",
    "Athletico-PR": "https://logodetimes.com/wp-content/uploads/athletico-paranaense.png",
    "Atlético-MG": "https://logodetimes.com/wp-content/uploads/atletico-mineiro.png",
    "Atlético-GO": "https://logodetimes.com/wp-content/uploads/atletico-goianiense.png",
    "Avaí": "https://logodetimes.com/wp-content/uploads/avai.png",
    "Bahia": "https://logodetimes.com/wp-content/uploads/bahia.png",
    "Botafogo": "https://logodetimes.com/wp-content/uploads/botafogo.png",
    "Botafogo-SP": "https://logodetimes.com/wp-content/uploads/botafogo-sp.png",
    "Bragantino": "https://logodetimes.com/wp-content/uploads/red-bull-bragantino.png",
    "Ceará": "https://logodetimes.com/wp-content/uploads/ceara.png",
    "Chapecoense": "https://logodetimes.com/wp-content/uploads/chapecoense.png",
    "Corinthians": "https://logodetimes.com/wp-content/uploads/corinthians.png",
    "Coritiba": "https://logodetimes.com/wp-content/uploads/coritiba.png",
    "CRB": "https://logodetimes.com/wp-content/uploads/crb.png",
    "Criciúma": "https://logodetimes.com/wp-content/uploads/criciuma.png",
    "Cruzeiro": "https://logodetimes.com/wp-content/uploads/cruzeiro.png",
    "Cuiabá": "https://logodetimes.com/wp-content/uploads/cuiaba.png",
    "Flamengo": "https://logodetimes.com/wp-content/uploads/flamengo.png",
    "Fluminense": "https://logodetimes.com/wp-content/uploads/fluminense.png",
    "Fortaleza": "https://logodetimes.com/wp-content/uploads/fortaleza.png",
    "Goiás": "https://logodetimes.com/wp-content/uploads/goias-esporte-clube.png",
    "Grêmio": "https://logodetimes.com/wp-content/uploads/gremio.png",
    "Internacional": "https://logodetimes.com/wp-content/uploads/internacional.png",
    "Juventude": "https://logodetimes.com/wp-content/uploads/juventude-rs.png",
    "Londrina": "https://logodetimes.com/wp-content/uploads/londrina.png",
    "Mirassol": "https://logodetimes.com/wp-content/uploads/mirassol.png",
    "Náutico": "https://logodetimes.com/wp-content/uploads/nautico.png",
    "Novorizontino": "https://logodetimes.com/wp-content/uploads/gremio-novorizontino.png",
    "Operário-PR": "https://logodetimes.com/wp-content/uploads/operario-pr.png",
    "Palmeiras": "https://logodetimes.com/wp-content/uploads/palmeiras.png",
    "Ponte Preta": "https://logodetimes.com/wp-content/uploads/ponte-preta.png",
    "Remo": "https://logodetimes.com/wp-content/uploads/remo.png",
    "Santos": "https://logodetimes.com/wp-content/uploads/santos.png",
    "São Bernardo": "https://logodetimes.com/wp-content/uploads/sao-bernardo.png",
    "São Paulo": "https://logodetimes.com/wp-content/uploads/sao-paulo.png",
    "Sport": "https://logodetimes.com/wp-content/uploads/sport-recife.png",
    "Vasco da Gama": "https://logodetimes.com/wp-content/uploads/vasco-da-gama.png",
    "Vila Nova": "https://logodetimes.com/wp-content/uploads/vila-nova.png",
    "Athletic Club": "https://upload.wikimedia.org/wikipedia/commons/f/f8/Athletic_Club_%28Minas_Gerais%29.svg",
    "EC Vitória": "https://logodetimes.com/wp-content/uploads/vitoria.png"
}

# Links das imagens dos títulos
TROPHY_IMAGES = {
    "Copa Libertadores": "https://www.palmeiras.com.br/wp-content/uploads/2019/08/libertadores-galeria-de-titulos.png",
    "Campeonato Brasileiro": "https://www.palmeiras.com.br/wp-content/uploads/2019/08/06.png",
    "Copa do Brasil": "https://www.palmeiras.com.br/wp-content/uploads/2019/08/02-1.png",
    "Supercopa do Brasil": "https://www.palmeiras.com.br/wp-content/uploads/2023/01/Supercopa-do-Brasil-2023-PNG.png",
    "Recopa Sul-Americana": "https://www.palmeiras.com.br/wp-content/uploads/2022/03/recopa.png",
    "Mundial de Clubes": "https://i.pinimg.com/originals/8f/cf/62/8fcf62853f18cde309c1a6a1d6e2f625.png",
    "Copa Sul-Americana": "https://worried-lime-d3mky6noyh.edgeone.app/5b8ee48fc70fd96d67147d6c59658ef6-removebg-preview.png",
    "Copa Mercosul": "https://www.verdazzo.com.br/wp-content/uploads/2020/06/1998-mercosul.png",
    "Copa Conmebol": "https://realistic-turquoise-hrkqjj8wlv.edgeone.app/images-removebg-preview%20(2).png",
    "Supercopa Libertadores": "https://junior-jade-xacywjlwml.edgeone.app/trofeu_supercopa_libertadores-removebg-preview.png"
}

# Cores oficiais aproximadas dos times
TEAM_COLORS = {
    "Flamengo": "#D00027",        # Vermelho oficial
    "Palmeiras": "#006437",       # Verde escuro oficial
    "Santos": "#FFFFFF",          # Branco predominante
    "São Paulo": "#E30613",       # Vermelho SPFC
    "Corinthians": "#111111",     # Preto predominante
    "Grêmio": "#005CA9",          # Azul oficial
    "Internacional": "#C8102E",   # Vermelho Inter
    "Cruzeiro": "#0033A0",        # Azul oficial
    "Atlético-MG": "#000000",     # Preto
    "Botafogo": "#000000",        # Preto
    "Vasco da Gama": "#000000",   # Preto predominante
    "Fluminense": "#7A0026",      # Grená
    "Bahia": "#0033A0",           # Azul oficial
    "Athletico-PR": "#C8102E",    # Vermelho
    "Sport": "#C8102E",           # Vermelho
    "Juventude": "#0B7A3B",       # Verde
    "Fortaleza": "#0055A4",       # Azul
    "Ceará": "#000000",           # Preto
    "Goiás": "#006B3F",           # Verde
    "América-MG": "#008751",      # Verde
    "Coritiba": "#006437",        # Verde
    "Chapecoense": "#047A3A",     # Verde
    "Avaí": "#0055A4"             # Azul
}

# Dicionário de títulos por time
TEAM_TITLES = {
    "Internacional": {
        "titles": [
            {"nome": "Mundial de Clubes", "ano": "2006", "imagem": TROPHY_IMAGES["Mundial de Clubes"]},
            {"nome": "Copa Libertadores", "ano": "2006, 2010", "imagem": TROPHY_IMAGES["Copa Libertadores"]},
            {"nome": "Copa Sul-Americana", "ano": "2008", "imagem": TROPHY_IMAGES["Copa Sul-Americana"]},
            {"nome": "Recopa Sul-Americana", "ano": "2007, 2011", "imagem": TROPHY_IMAGES["Recopa Sul-Americana"]},
            {"nome": "Campeonato Brasileiro", "ano": "1975, 1976, 1979", "imagem": TROPHY_IMAGES["Campeonato Brasileiro"]},
            {"nome": "Copa do Brasil", "ano": "1992", "imagem": TROPHY_IMAGES["Copa do Brasil"]}
        ]
    },
    "Flamengo": {
        "titles": [
            {"nome": "Mundial de Clubes", "ano": "1981", "imagem": TROPHY_IMAGES["Mundial de Clubes"]},
            {"nome": "Copa Libertadores", "ano": "1981, 2019, 2022" "2025", "imagem": TROPHY_IMAGES["Copa Libertadores"]},
            {"nome": "Copa Mercosul", "ano": "1999", "imagem": TROPHY_IMAGES["Copa Mercosul"]},
            {"nome": "Campeonato Brasileiro", "ano": "1980, 1982, 1983, 1992, 2009, 2019, 2020", "imagem": TROPHY_IMAGES["Campeonato Brasileiro"]},
            {"nome": "Copa do Brasil", "ano": "1990, 2006, 2013, 2022", "imagem": TROPHY_IMAGES["Copa do Brasil"]},
            {"nome": "Supercopa do Brasil", "ano": "2020, 2021", "imagem": TROPHY_IMAGES["Supercopa do Brasil"]},
            {"nome": "Recopa Sul-Americana", "ano": "2020", "imagem": TROPHY_IMAGES["Recopa Sul-Americana"]}
        ]
    },
    "Palmeiras": {
        "titles": [
            {"nome": "Copa Libertadores", "ano": "1999, 2020, 2021", "imagem": TROPHY_IMAGES["Copa Libertadores"]},
            {"nome": "Copa Mercosul", "ano": "1998", "imagem": TROPHY_IMAGES["Copa Mercosul"]},
            {"nome": "Campeonato Brasileiro", "ano": "1960, 1967, 1967, 1969, 1972, 1973, 1993, 1994, 2016, 2018, 2022", "imagem": TROPHY_IMAGES["Campeonato Brasileiro"]},
            {"nome": "Copa do Brasil", "ano": "1998, 2012, 2015, 2020", "imagem": TROPHY_IMAGES["Copa do Brasil"]},
            {"nome": "Recopa Sul-Americana", "ano": "2022", "imagem": TROPHY_IMAGES["Recopa Sul-Americana"]}
        ]
    },
    "São Paulo": {
        "titles": [
            {"nome": "Mundial de Clubes", "ano": "1992, 1993, 2005", "imagem": TROPHY_IMAGES["Mundial de Clubes"]},
            {"nome": "Copa Libertadores", "ano": "1992, 1993, 2005", "imagem": TROPHY_IMAGES["Copa Libertadores"]},
            {"nome": "Copa Sul-Americana", "ano": "2012", "imagem": TROPHY_IMAGES["Copa Sul-Americana"]},
            {"nome": "Supercopa Libertadores", "ano": "1993", "imagem": TROPHY_IMAGES["Supercopa Libertadores"]},
            {"nome": "Copa Conmebol", "ano": "1994", "imagem": TROPHY_IMAGES["Copa Conmebol"]},
            {"nome": "Campeonato Brasileiro", "ano": "1977, 1986, 1991, 2006, 2007, 2008", "imagem": TROPHY_IMAGES["Campeonato Brasileiro"]},
            {"nome": "Copa do Brasil", "ano": "2023", "imagem": TROPHY_IMAGES["Copa do Brasil"]},
            {"nome": "Recopa Sul-Americana", "ano": "1993, 1994", "imagem": TROPHY_IMAGES["Recopa Sul-Americana"]}
        ]
    },
    "Corinthians": {
        "titles": [
            {"nome": "Mundial de Clubes", "ano": "2000, 2012", "imagem": TROPHY_IMAGES["Mundial de Clubes"]},
            {"nome": "Copa Libertadores", "ano": "2012", "imagem": TROPHY_IMAGES["Copa Libertadores"]},
            {"nome": "Recopa Sul-Americana", "ano": "2013", "imagem": TROPHY_IMAGES["Recopa Sul-Americana"]},
            {"nome": "Campeonato Brasileiro", "ano": "1990, 1998, 1999, 2005, 2011, 2015, 2017", "imagem": TROPHY_IMAGES["Campeonato Brasileiro"]},
            {"nome": "Copa do Brasil", "ano": "1995, 2002, 2009", "imagem": TROPHY_IMAGES["Copa do Brasil"]},
            {"nome": "Supercopa do Brasil", "ano": "1991", "imagem": TROPHY_IMAGES["Supercopa do Brasil"]}
        ]
    },
    "Grêmio": {
        "titles": [
            {"nome": "Mundial de Clubes", "ano": "1983", "imagem": TROPHY_IMAGES["Mundial de Clubes"]},
            {"nome": "Copa Libertadores", "ano": "1983, 1995, 2017", "imagem": TROPHY_IMAGES["Copa Libertadores"]},
            {"nome": "Recopa Sul-Americana", "ano": "1996, 2018", "imagem": TROPHY_IMAGES["Recopa Sul-Americana"]},
            {"nome": "Campeonato Brasileiro", "ano": "1981, 1996", "imagem": TROPHY_IMAGES["Campeonato Brasileiro"]},
            {"nome": "Copa do Brasil", "ano": "1989, 1994, 1997, 2001, 2016", "imagem": TROPHY_IMAGES["Copa do Brasil"]},
            {"nome": "Copa Sul-Americana", "ano": "2018", "imagem": TROPHY_IMAGES["Copa Sul-Americana"]}
        ]
    },
    "Santos": {
        "titles": [
            {"nome": "Mundial de Clubes", "ano": "1962, 1963", "imagem": TROPHY_IMAGES["Mundial de Clubes"]},
            {"nome": "Copa Libertadores", "ano": "1962, 1963, 2011", "imagem": TROPHY_IMAGES["Copa Libertadores"]},
            {"nome": "Recopa Sul-Americana", "ano": "2012", "imagem": TROPHY_IMAGES["Recopa Sul-Americana"]},
            {"nome": "Copa Conmebol", "ano": "1998", "imagem": TROPHY_IMAGES["Copa Conmebol"]},
            {"nome": "Campeonato Brasileiro", "ano": "1961, 1962, 1963, 1964, 1965, 1968, 2002, 2004", "imagem": TROPHY_IMAGES["Campeonato Brasileiro"]},
            {"nome": "Copa do Brasil", "ano": "2010", "imagem": TROPHY_IMAGES["Copa do Brasil"]}
        ]
    },
    "Cruzeiro": {
        "titles": [
            {"nome": "Copa Libertadores", "ano": "1976, 1997", "imagem": TROPHY_IMAGES["Copa Libertadores"]},
            {"nome": "Recopa Sul-Americana", "ano": "1998", "imagem": TROPHY_IMAGES["Recopa Sul-Americana"]},
            {"nome": "Supercopa Libertadores", "ano": "1991, 1992", "imagem": TROPHY_IMAGES["Supercopa Libertadores"]},
            {"nome": "Campeonato Brasileiro", "ano": "1966, 2003, 2013, 2014", "imagem": TROPHY_IMAGES["Campeonato Brasileiro"]},
            {"nome": "Copa do Brasil", "ano": "1993, 1996, 2000, 2003, 2017, 2018", "imagem": TROPHY_IMAGES["Copa do Brasil"]}
        ]
    },
    "Atlético-MG": {
        "titles": [
            {"nome": "Copa Libertadores", "ano": "2013", "imagem": TROPHY_IMAGES["Copa Libertadores"]},
            {"nome": "Recopa Sul-Americana", "ano": "2014", "imagem": TROPHY_IMAGES["Recopa Sul-Americana"]},
            {"nome": "Copa Conmebol", "ano": "1992", "imagem": TROPHY_IMAGES["Copa Conmebol"]},
            {"nome": "Campeonato Brasileiro", "ano": "1937, 1971, 2021", "imagem": TROPHY_IMAGES["Campeonato Brasileiro"]},
            {"nome": "Copa do Brasil", "ano": "2014, 2021", "imagem": TROPHY_IMAGES["Copa do Brasil"]}
        ]
    },
    "Botafogo": {
        "titles": [
            {"nome": "Copa Conmebol", "ano": "1993", "imagem": TROPHY_IMAGES["Copa Conmebol"]},
            {"nome": "Campeonato Brasileiro", "ano": "1968, 1995", "imagem": TROPHY_IMAGES["Campeonato Brasileiro"]}
        ]
    },
    "Vasco da Gama": {
        "titles": [
            {"nome": "Copa Libertadores", "ano": "1998", "imagem": TROPHY_IMAGES["Copa Libertadores"]},
            {"nome": "Copa Mercosul", "ano": "2000", "imagem": TROPHY_IMAGES["Copa Mercosul"]},
            {"nome": "Campeonato Brasileiro", "ano": "1974, 1989, 1997, 2000", "imagem": TROPHY_IMAGES["Campeonato Brasileiro"]},
            {"nome": "Copa do Brasil", "ano": "2011", "imagem": TROPHY_IMAGES["Copa do Brasil"]}
        ]
    },
    "Fluminense": {
        "titles": [
            {"nome": "Copa Libertadores", "ano": "2023", "imagem": TROPHY_IMAGES["Copa Libertadores"]},
            {"nome": "Copa do Brasil", "ano": "2007", "imagem": TROPHY_IMAGES["Copa do Brasil"]},
            {"nome": "Campeonato Brasileiro", "ano": "1970, 1984, 2010, 2012", "imagem": TROPHY_IMAGES["Campeonato Brasileiro"]}
        ]
    },
    "Bahia": {
        "titles": [
            {"nome": "Campeonato Brasileiro", "ano": "1959, 1988", "imagem": TROPHY_IMAGES["Campeonato Brasileiro"]}
        ]
    },
    "Athletico-PR": {
        "titles": [
            {"nome": "Copa Sul-Americana", "ano": "2018, 2021", "imagem": TROPHY_IMAGES["Copa Sul-Americana"]},
            {"nome": "Copa do Brasil", "ano": "2019", "imagem": TROPHY_IMAGES["Copa do Brasil"]},
            {"nome": "Campeonato Brasileiro", "ano": "2001", "imagem": TROPHY_IMAGES["Campeonato Brasileiro"]}
        ]
    },
    "Sport": {
        "titles": [
            {"nome": "Copa do Brasil", "ano": "2008", "imagem": TROPHY_IMAGES["Copa do Brasil"]}
        ]
    },
    "Juventude": {
        "titles": [
            {"nome": "Copa do Brasil", "ano": "1999", "imagem": TROPHY_IMAGES["Copa do Brasil"]}
        ]
    }
}

@app.route("/", methods=["GET", "POST"])
def home():
    team = None
    games = []
    titles = []
    team_description = ""
    team_image = ""
    team_color = "#3b82f6"  # cor padrão

    if request.method == "POST":
        team_name = request.form["team_name"].strip()
        
        try:
            # Buscar time na API
            url_team = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}/searchteams.php?t={team_name}"
            response = requests.get(url_team, timeout=5).json()
            
            if response.get("teams"):
                team = response["teams"][0]
                team_id = team["idTeam"]
                team_display_name = team.get("strTeam", "")
                
                # Pegar cor do time
                for nome_time, cor in TEAM_COLORS.items():
                    if nome_time.lower() in team_display_name.lower():
                        team_color = cor
                        break
                
                # Buscar escudo (prioridade para seus links)
                for nome_time in TEAM_BADGES:
                    if nome_time.lower() in team_display_name.lower() or team_display_name.lower() in nome_time.lower():
                        team_image = TEAM_BADGES[nome_time]
                        break
                
                if not team_image:
                    team_image = team.get("strTeamBadge") or team.get("strTeamLogo")
                
                # Descrição em português
                if team.get("strDescriptionPT"):
                    team_description = team["strDescriptionPT"]
                elif team.get("strDescriptionEN"):
                    team_description = team["strDescriptionEN"]
                else:
                    team_description = f"O {team.get('strTeam', 'time')} é um clube de futebol brasileiro fundado em {team.get('intFormedYear', 'ano desconhecido')}. Manda seus jogos no estádio {team.get('strStadium', 'estádio desconhecido')}."
                
                # Últimos jogos
                url_games = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}/eventslast.php?id={team_id}"
                games_response = requests.get(url_games, timeout=5).json()
                games = games_response.get("results", [])[:5]
                
                # Títulos
                for key in TEAM_TITLES:
                    if key.lower() in team_display_name.lower() or team_display_name.lower() in key.lower():
                        titles = TEAM_TITLES[key]["titles"]
                        break
                
                if not titles:
                    for key in TEAM_TITLES:
                        if key.lower() in team_name.lower():
                            titles = TEAM_TITLES[key]["titles"]
                            break
                            
        except Exception as e:
            print(f"Erro na API: {e}")
            
    return render_template("index.html", 
                         team=team, 
                         games=games, 
                         titles=titles, 
                         team_description=team_description, 
                         team_image=team_image,
                         team_color=team_color)

@app.route("/api/suggest", methods=["GET"])
def suggest_teams():
    term = request.args.get("term", "").lower()
    if len(term) < 3:
        return jsonify([])
    
    suggestions = []
    for team_name in TEAM_BADGES.keys():
        if term in team_name.lower():
            suggestions.append(team_name)
    
    return jsonify(suggestions[:5])  # Limita a 5 sugestões

if __name__ == "__main__":
    app.run(debug=True)