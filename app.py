from flask import Flask, request, jsonify
import pyodbc  
from flask_cors import CORS  

app = Flask(__name__)
CORS(app)  

def connect_db():
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'SERVER=BELLE\\SQLEXPRESS;'
                      'DATABASE=LivroRecom;'
                      'Trusted_Connection=yes;')
    return conn

def store_responses(responses):
    conn = connect_db()
    cursor = conn.cursor()

    recommendation = recommend_book(responses)
    book_title = recommendation.get("book")

    sql = """
    INSERT INTO Respostas (pergunta_1, pergunta_2, pergunta_3, pergunta_4, pergunta_5, 
                           pergunta_6, pergunta_7, pergunta_8, pergunta_9, pergunta_10, livro_recomendado)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(sql, (
        responses.get('pergunta_1'), responses.get('pergunta_2'), responses.get('pergunta_3'),
        responses.get('pergunta_4'), responses.get('pergunta_5'), responses.get('pergunta_6'),
        responses.get('pergunta_7'), responses.get('pergunta_8'), responses.get('pergunta_9'),
        responses.get('pergunta_10'), book_title
    ))
    conn.commit()
    conn.close()

def calculate_percentage_for_book(book_title):
    conn = connect_db()
    cursor = conn.cursor()

    sql = "SELECT COUNT(*) FROM Respostas WHERE livro_recomendado = ?"
    cursor.execute(sql, (book_title,))
    count = cursor.fetchone()[0]

    sql_total = "SELECT COUNT(*) FROM Respostas"
    cursor.execute(sql_total)
    total = cursor.fetchone()[0]

    conn.close()

    if total > 0:
        percentage = (count / total) * 100
    else:
        percentage = 0

    return percentage

def recommend_book(responses):
    counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0}
    for answer in responses.values():
        counts[answer] += 1

    if counts['A'] > counts['B'] and counts['A'] > counts['C']:
        return {
            "book": "O Grande Gatsby (F. Scott Fitzgerald)",
            "justification": "Para aqueles que estão em um estado emocional de paz e tranquilidade, O Grande Gatsby é um reflexo fascinante da busca pelo sonho e pela felicidade. Gatsby, o personagem principal, é um símbolo de esperança e de aspirações, sempre tentando alcançar um ideal de felicidade que parece à primeira vista estar ao seu alcance, mas que se revela ilusório. A obra traz à tona a reflexão sobre o que é realmente importante na vida e como as nossas próprias expectativas podem ser distorcidas por ideais irreais. Embora Gatsby represente alguém que vive em busca de um futuro melhor, sua jornada traz a lição de que nem sempre o que desejamos corresponde ao que realmente precisamos para ser felizes. Este livro pode, então, levar você a refletir sobre suas próprias aspirações e como equilibrar as metas externas com a verdadeira realização interior."
        }
    elif counts['B'] > counts['C'] and counts['B'] > counts['A']:
        return {
            "book": "Memórias Póstumas de Brás Cubas (Machado de Assis)",
            "justification": "O personagem principal, Brás Cubas, narra sua vida pós-morte, refletindo sobre seus próprios erros, frustrações e a futilidade das buscas humanas. A obra mistura humor e tragédia, mostrando como as escolhas que fazemos muitas vezes não nos levam à felicidade, mas à dúvida e à desesperança. Para aqueles que estão em um momento de incerteza, o livro oferece uma crítica feroz à sociedade e às nossas próprias limitações, enquanto expõe as preocupações que surgem diante das nossas falhas e expectativas frustradas. A ironia de Brás Cubas e seu olhar sarcástico sobre o mundo podem trazer uma sensação de alívio ao perceber que todos compartilham das mesmas angústias, e, ao mesmo tempo, provocam uma reflexão sobre como encontrar um propósito que transcenda os medos e ansiedades cotidianas."
        }
    elif counts['C'] > counts['A'] and counts['C'] > counts['B']:
        return {
            "book": "Ensaio Sobre a Cegueira (José Saramago)",
            "justification": "Quando a tristeza e o desânimo tomam conta, Ensaio Sobre a Cegueira é uma obra que ajuda a encontrar sentido mesmo em meio ao caos. O livro de Saramago narra a história de uma sociedade que perde repentinamente a visão, levando seus habitantes a enfrentar uma luta pela sobrevivência em um mundo sem orientação. Para quem está se sentindo perdido ou desmotivado, a cegueira metafórica dos personagens pode ser vista como uma representação de como, muitas vezes, nos sentimos desconectados de nós mesmos e do mundo ao nosso redor. O livro explora o desespero e a falta de direção, mas também é um convite à reflexão sobre como podemos, mesmo nas circunstâncias mais desoladoras, encontrar um caminho para a empatia e para a renovação pessoal. Ele mostra como a vulnerabilidade e a perda podem ser fontes de transformação, levando-nos a descobrir novos significados em nossas vidas, mesmo quando tudo parece obscurecido."
        }
    elif counts['D'] > counts['A'] and counts['D'] > counts['B']:
        return {
            "book": "Romeu e Julieta (William Shakespeare)",
            "justification": "Para aqueles que se sentem empolgados e otimistas, Romeu e Julieta captura perfeitamente o entusiasmo e a intensidade da paixão jovem. A história de dois jovens apaixonados que enfrentam obstáculos imensuráveis para viver seu amor nos ensina sobre o poder de se entregar aos sentimentos mais profundos e sobre os riscos de idealizar um amor perfeito. Enquanto o livro reflete a emoção pura da juventude, também nos alerta sobre as consequências de decisões impulsivas e da intensidade de emoções não equilibradas. A obra de Shakespeare mostra que, embora a empolgação e o entusiasmo sejam vitais para a vida, é fundamental também refletir sobre as implicações de nossas ações e decisões. Para quem está otimista e cheio de energia, Romeu e Julieta pode servir de lembrete de que o amor é ao mesmo tempo libertador e complexo, e deve ser vivido com sabedoria e consciência."
        }
    elif counts['E'] > counts['A'] and counts['E'] > counts['F']:
        return {
            "book": "O Velho e o Mar (Ernest Hemingway)",
            "justification": "Quando você se encontra em um estado de cansaço e exaustão, O Velho e o Mar é uma leitura que transmite uma poderosa lição sobre perseverança. O livro acompanha a luta de Santiago, um velho pescador que enfrenta um enorme peixe em uma batalha solitária e árdua, simbolizando a luta de cada ser humano contra suas próprias dificuldades e limitações. Para quem está exausto, essa história pode ser um alento, mostrando que, mesmo em momentos de grande fadiga, a luta por um objetivo e a busca pela dignidade nunca devem ser abandonadas. O velho pescador, apesar de todas as adversidades, ensina que o verdadeiro valor da vida está em como enfrentamos nossos desafios, com coragem e resiliência, e que cada esforço, por mais árduo que seja, tem um significado e uma recompensa interior. O livro pode inspirar a encontrar forças no silêncio da luta pessoal e na beleza da perseverança, mesmo quando tudo parece estar contra nós."
        }
    elif counts['F'] > counts['A'] and counts['F'] > counts['B']:
        return {
            "book": "Crime e Castigo (Fiódor Dostoiévski)",
            "justification": "O protagonista, Raskólnikov, é um jovem que comete um assassinato na tentativa de justificar um mal maior e acaba imerso em uma luta moral e emocional que o consome completamente. O livro explora as consequências da culpa e do arrependimento, mostrando como nossas escolhas podem ser imbuídas de racionalizações que, quando confrontadas com a realidade, revelam um profundo vazio. Para quem está frustrado e irritado, a obra oferece uma oportunidade de introspecção, permitindo questionar o que realmente nos motiva e como nossas emoções mais intensas podem nos levar a ações que, por fim, apenas ampliam o sofrimento. Crime e Castigo oferece a chance de refletir sobre a necessidade de reconciliação consigo mesmo e com o mundo ao redor, trazendo à tona a importância da transformação interior para superar o desespero e a frustração."
        }
    elif counts['A'] == counts['B']:
        return {
            "book": "Orgulho e Preconceito (Jane Austen)",
            "justification": "Quando você se encontra em um estado de tranquilidade, mas com uma leve sensação de incerteza sobre o que o futuro pode reservar, Orgulho e Preconceito se torna uma leitura essencial. A obra de Jane Austen não é apenas sobre o romance entre Elizabeth Bennet e Mr. Darcy, mas sobre o processo de autodescoberta, onde as escolhas pessoais se entrelaçam com as expectativas da sociedade. O livro retrata como o orgulho e o preconceito moldam nossas relações, mas também como a evolução interna, o crescimento pessoal e a capacidade de questionar nossas crenças  podem levar à transformação. O romance convida você a refletir sobre como as decisões que tomamos, muitas vezes impulsionadas por medos ou julgamentos precipitados, podem ser questionadas à medida que nos conhecemos melhor e entendemos nossas reais necessidades e desejos."
        }
    elif counts['C'] == counts['B']:
        return {
            "book": "A Paixão Segundo GH (Clarice Lispector)",
            "justification": "Se você está em um momento de frustração ou desilusão, A Paixão Segundo GH de Clarice Lispector é uma escolha intensa. A obra aborda questões de identidade, autoconhecimento e transformação interior, com uma protagonista que se vê diante de uma experiência perturbadora que desencadeia um turbilhão de questionamentos existenciais. Para quem se sente perdido e busca respostas, a narrativa oferece uma reflexão desconfortável, mas necessária, sobre o que significa ser humano e como a busca por sentido pode ser ao mesmo tempo dolorosa e libertadora. A autora cria um ambiente de introspecção profunda, onde o leitor é desafiado a confrontar suas próprias inseguranças e buscar a verdadeira essência do ser."
        }
    elif counts['D'] == counts['E']:
        return {
            "book": "Babel (R.F. Kuang)",
            "justification": "Quando a empolgação e o desejo de conquista se misturam com o cansaço físico e emocional, Babel é a leitura ideal. O livro de R.F. Kuang traz à tona temas de resistência, poder e identidade, enquanto narra uma história de jovens que desafiam estruturas de poder e buscam algo maior do que a simples sobrevivência. Para quem se sente exausto, mas ainda mantém a energia de quem enfrenta grandes desafios, Babel oferece uma reflexão crítica sobre as forças que nos oprimem e como podemos resistir e lutar por um mundo mais justo, mesmo quando estamos em nossos limites."
        }
    elif counts['C'] == counts['D']:
        return {
            "book": "Torto Arado (Itamar Vieira Júnior)",
            "justification": "Se você está em um momento de tristeza e incerteza, mas ainda busca a força para seguir em frente, Torto Arado é uma leitura inspiradora. Ambientada no sertão nordestino, a obra de Itamar Vieira Júnior explora questões de identidade, memória e superação, através da história de duas irmãs que enfrentam adversidades imensas. O livro aborda resistência, luta pela dignidade e busca por pertencimento. Para quem está em dúvida sobre qual caminho seguir, Torto Arado oferece uma mensagem: mesmo quando a vida parece difícil e os obstáculos parecem intransponíveis, a perseverança e a conexão com nossas raízes podem nos ajudar a encontrar a paz e a compreensão de quem realmente somos."
        }
    elif counts['A'] == counts['C']:
        return {
            "book": "O Retrato de Dorian Gray (Oscar Wilde)",
            "justification": "Quando você se sente confiante, mas com uma leve sombra de tristeza ou dúvida sobre suas escolhas, O Retrato de Dorian Gray pode ser um reflexo dessa dualidade. O romance de Oscar Wilde explora a busca pela perfeição e o desejo de juventude eterna, levando o protagonista a fazer escolhas que o afastam de sua verdadeira essência. A obra oferece aborda os perigos de se perseguir uma imagem idealizada, sem considerar as consequências das escolhas superficiais. Para quem está em um momento de confiança misturada com dúvidas, o livro serve como um alerta sobre como a aparência e a busca incessante pela perfeição podem corroer o que é genuíno e verdadeiro em nós."
        }
    elif counts['F'] == counts['B']:
        return {
            "book": "Noites Brancas (Fiódor Dostoiévski)",
            "justification": "Se você está passando por um momento de frustração, cheio de dúvidas intensas, Noites Brancas de Dostoiévski pode ser uma leitura esclarecedora. O livro segue a história de um homem solitário que se perde nas suas próprias idealizações sobre o amor e a vida. Ele reflete profundamente sobre suas emoções e a busca por algo que lhe dê significado, mas sem nunca encontrar um propósito definitivo. Para quem está se sentindo perdido e em busca de algo mais, Noites Brancas oferece uma reflexão sobre as expectativas irreais que construímos em nossa mente e como o amor e a vida podem ser mais complexos e fugidios do que imaginamos. A obra é uma exploração sensível da solidão e da busca por sentido, algo profundamente relevante quando estamos tomados pela dúvida e pela frustração."
        }
    elif counts['E'] == counts['F']:
        return {
            "book": "Battle Royale (Koushun Takami)",
            "justification": "Quando a exaustão e a frustração dominam, Battle Royale oferece uma leitura intensa e reflexiva. A história, que se passa em um futuro distópico, acompanha um grupo de estudantes que são forçados a lutar até a morte em uma competição brutal. Para quem está se sentindo exausto e frustrado, o livro reflete sobre a opressão do sistema social e os limites humanos diante de circunstâncias extremas. A luta pela sobrevivência, em um contexto de extrema violência e alienação, traz à tona as questões sobre o que nos motiva a continuar lutando quando tudo parece perdido. Battle Royale é uma exploração brutal da resistência humana e da necessidade de questionar as estruturas de poder que nos controlam, sendo uma escolha adequada para aqueles que, em sua exaustão, buscam entender a complexidade da luta pela liberdade e pelo sentido da vida."
        }

    return {
        "book": "Percy Jackson e os Olimpianos (Rick Riordan)",
        "justification": "Não foi possível determinar um estado emocional específico, mas aqui está um livro que pode agradar em qualquer circunstância."
    }

@app.route('/submit_responses', methods=['POST'])
def submit_responses():
    responses = request.json  
    store_responses(responses)

    recommendation = recommend_book(responses)
    book_title = recommendation.get("book")

    percentage = calculate_percentage_for_book(book_title)

    return jsonify({
        'recommendation': recommendation,
        'percentage': percentage
    })

if __name__ == '__main__':
    app.run(debug=True)
