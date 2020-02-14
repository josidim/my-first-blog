from django.shortcuts import render, redirect
import csv, io
from django.contrib import messages

# Create your views here.


from valida.models import t_face_cnefe


def index(request):
	list = t_face_cnefe.objects.all()[:15]
	return render(request, 'index.html', {'list': list})


def upload_csv(request):
	return render(request, 'upload_csv.html')	
	
	

	
def upload_csv(request):
	#msg = messages.get_messages(request)
	check = [] #retorna o resultado da consulta ao banco de dados
	linhas = [] #guarda das linhas do csv
	data = {}
	total = 0 #retorna a quantidade de registros afetados pela consulta ao banco
	lista_tipos = ["ACAMPAMENTO", "ACESSO", "ACUDE", "ADRO", "AEROPORTO","AFLUENTE","AGLOMERADO","AGROVILA","ALAGADO","ALAMEDA","ALDEIA","ALEIA","ALTO","ANEL","ANTIGA","ANTIGO","AREA","AREAL","ARRAIAL","ARROIO","ARTERIA",
	"ASSENTAMENTO","ATALHO","ATERRO","AUTODROMO","AVENIDA","BAIA","BAIRRO","BAIXA","BAIXADA","BAIXADAO","BAIXAO","BAIXO","BALAO","BALNEARIO","BARRA","BARRAGEM","BARRANCA","BARRANCO","BARREIRO","BARRO","BECO","BEIRA","BEIRADA",
	"BELVEDERE","BLOCO","BOCAINA","BOQUEIRAO","BOSQUE","BOULEVARD","BREJO","BURACO","CABECEIRA","CACHOEIRA","CACHOEIRINHA","CAIS","CALCADA","CALCADAO","CAMINHO","CAMPO","CANAL","CANTEIRO","CAPAO","CAPOEIRA","CARTODROMO","CENTRAL",
	"CENTRO","CERCA","CERRADO","CERRO","CHACARA","CHAPADA","CHAPADAO","CHARCO","CIDADE","CIRCULAR","COHAB","COLINA","COLONIA","COMUNIDADE","CONDOMINIO","CONJUNTO","CONTINUACAO","CONTORNO","CORREDOR","CORREGO","COSTA","COXILHA",
	"CRUZAMENTO","DESCIDA","DESVIO","DIQUE","DISTRITO","DIVISA","DIVISAO","DIVISOR","EDF","EDIFICIO","EIXO","ELEVADO","ENCOSTA","ENGENHO","ENSEADA","ENTRADA","ENTREPOSTO","ENTRONCAMENTO","ESCADA","ESCADAO","ESCADARIA","ESCADINHA",
	"ESPIGAO","ESPLANADA","ESQUINA","ESTACAO","ESTACIONAMENTO","ESTADIO","ESTANCIA","ESTRADA","EXTENSAO","FAIXA","FAVELA","FAZENDA","FEIRA","FERROVIA","FINAL","FLORESTA","FOLHA","FONTE","FORTALEZA","FREGUESIA","FUNDOS","FURO",
	"GALERIA","GAMELEIRA","GARIMPO","GLEBA","GRANJA","GROTA","HABITACIONAL","HARAS","HIPODROMO","HORTO","IGARAPE","ILHA","INAPLICÁVEL","INVASAO","JARDIM","JARDINETE","LADEIRA","LADO","LAGO","LAGOA","LAGOINHA","LARGO","LATERAL",
	"LEITO","LIGACAO","LIMEIRA","LIMITE","LIMITES","LINHA","LOTE","LOTEAMENTO","LUGAREJO","MALOCA","MANANCIAL","MANGUE","MARGEM","MARGENS","MARGINAL","MARINA","MATA","MATO","MODULO","MONTE","MORRO","MURO","NUCLEO","OCA","OLEODUTO",
	"OLHO","OLHOS","ORLA","OUTROS","PACO","PALAFITA","PANTANO","PARADA","PARADOURO","PARALELA","PARQUE","PARTICULAR","PASSAGEM","PASSARELA","PASSEIO","PASSO","PASTO","PATIO","PAVILHAO","PEDRA","PEDRAS","PEDREIRA","PENHASCO",
	"PERIMETRAL","PERIMETRO","PERTO","PLANALTO","PLATAFORMA","PONTA","PONTE","PONTO","PORTO","POSTO","POVOADO","PRACA","PRAIA","PROJECAO","PROJETADA","PROJETO","PROLONGAMENTO","PROPRIEDADE","PROXIMO","QUADRA","QUARTEIRAO",
	"QUILOMBO","QUILOMETRO","QUINTA","QUINTAS","RAMAL","RAMPA","RANCHO","RECANTO","REGIAO","REPRESA","RESIDENCIAL","RETA","RETIRO","RETORNO","RIACHAO","RIACHO","RIBANCEIRA","RIBEIRAO","RINCAO","RIO","ROCHA","ROCHEDO","RODOVIA",
	"ROTATORIA","ROTULA","RUA","RUELA","SACO","SAIDA","SANGA","SEDE","SEM","SERINGAL","SERRA","SERTAO","SERVIDAO","SETA","SETOR","SITIO","SOPE","SUBIDA","SUPERQUADRA","TAPERA","TERMINAL","TERRA","TERRENO","TERRENOS","TRANSVERSAL",
	"TRAVESSA","TRAVESSAO","TRAVESSIA","TRECHO","TREVO","TRILHA","TRILHO","TRILHOS","TRINCHEIRA","TUNEL","UNIDADE","USINA","VALA","VALAO","VALE","VARGEM","VARIANTE","VARZEA","VELODROMO","VEREDA","VERTENTE","VIA","VIADUTO","VICINAL",
	"VIELA","VILA","VILAREJO","VOLTA","ZONA","FORTE","LAMEIRA","NAO ESPECIFICADO","PENEDO","1a TRAVESSA DA RUA","2a TRAVESSA DA RUA","3a TRAVESSA DA RUA","4a TRAVESSA DA RUA","5a TRAVESSA DA RUA","1a TRAVESSA DA AVENIDA",
	"2a TRAVESSA DA AVENIDA","3a TRAVESSA DA AVENIDA","4a TRAVESSA DA AVENIDA","5a TRAVESSA DA AVENIDA"]
	#FIM LISTA DE TIPOS
	lista_titulos = ["ABADE", "ABADESSA", "ACADEMICO", "ADMINISTRADOR", "ADMINISTRADORA", "ADMONITOR", "ADVOGADA", "ADVOGADO", "AERONAUTA", "AGENTE", "AGRICULTOR", "GRIMENSOR", "AGRONOMO", "AJUDANTE", "ALCAIDE", "ALCAIDESSA",
"ALCAIDINA", "ALFAQUI", "ALFERES", "ALMIRANTE", "ALUNA", "ALUNO", "ANCIA", "ANCIAO", "ANSPECADA", "ANTISTE", "ANTISTITE", "APOSTOLO", "ARABI", "ARCEBISPO", "ARCEDIAGO", "ARCIPRESTE", "ARQUIDUQUE", "ARQUIDUQUESA", "ARQUITETA",
"ARQUITETO", "ARTESAO", "ARTISTA", "ASPIRANTE", "ASSESSOR", "ASSESSORA", "ATENDENTE", "ATLETA", "ATOR", "ATRIZ", "AVIADOR", "AVIADORA", "BABALAO", "BABALORIXA", "BACHAREL", "BANCARIA", "BANCARIO", "BANDEIRANTE", "BANDEIRANTES",
"BARAO", "BARNABITA", "BARONESA", "BISNETA", "BISNETO", "BISPO", "BOMBEIRO", "BONZO", "BOTO", "BRIGADEIRO", "CABO", "CABOCLA", "CABOCLO", "CACADOR", "CACIQUE", "CADETE", "CANONISA", "CANTOR", "CANTORA", "CAPELAO", "CAPITAO",
"CAPITAO AVIADOR", "CAPITAO MOR", "CAPITAO TENENTE", "CAPUCHINHO", "CARDEAL", "CARMELITA", "CARMELITANO", "CARPINTEIRO", "CARTEIRO", "CAVALHEIRO", "CHANCELER", "CHEFE", "CIENTISTA", "CINEASTA", "CIRURGIAO", "CLARISTA","CLERIGO",
"COLETOR", "COLUNISTA", "COMANDANTE", "COMBATENTE", "COMENDADEIRA", "COMENDADOR", "COMERCIANTE", "COMERCIARIA", "COMISSARIA", "COMISSARIO", "COMODORO", "COMPOSITOR", "COMPOSITORA", "CONDE", "CONDESSA", "CONEGO", "CONFESSOR",
"CONFRADE", "CONFREIRA", "CONSELHEIRA", "CONSELHEIRO", "CONSTRUTOR", "CONSUL", "CONSULESA", "CONSULTOR", "CONSULTORA", "CONTABILISTA", "CONTADOR", "CONTADORA", "CONTISTA", "CONTRA ALMIRANTE", "CORONEL", "CORRETOR", "CORRETORA",
"CRONISTA", "CUNHADA", "CUNHADO", "CURA", "CZAR", "CZARINA", "DAROES", "DEAO", "DECANO", "DEFENSOR PUBLICO", "DELEGADA", "DELEGADO", "DENOMINACAO", "DENTISTA", "DEPUTADA", "DEPUTADO", "DESEMBARGADOR", "DESENHISTA", "DESPACHANTE",
"DESPORTISTA", "DETETIVE", "DIACONISA", "DIACONO", "DICIONARISTA", "DIRETOR", "DIRETORA", "DOGARESA", "DOGARESSA", "DOGE", "DOGESA", "DOM", "DOMINICANO", "DONA", "DOUTOR", "DOUTORA", "DRUIDA", "DRUIDESA", "DRUIDISA", "DUQUE",
"DUQUESA", "ECONOMISTA", "ELETRICISTA", "EMBAIXADOR", "EMBAIXATRIZ", "ENFERMEIRA", "ENFERMEIRO", "ENGENHEIRA", "ENGENHEIRO", "EPISCOPISA", "ESCOTEIRO", "ESCRAVA", "ESCRAVO", "ESCRITOR", "ESCRITORA", "ESCRIVA", "ESCRIVAO", "ESTUDANTE",
"EVANGELISTA", "EVANGELIZADOR", "EVANGELIZADORA", "EXPEDICIONARIO", "FARMACEUTICA", "FARMACEUTICO", "FERROVIARIA", "FERROVIARIO", "FILHA", "FILHAS", "FILHO", "FILHOS", "FISCAL", "FISICO", "FOLCLORISTA", "FOTOGRAFA", "FOTOGRAFO",
"FRADE", "FREI", "FREIRA", "FREIRE", "FUNCIONARIA", "FUNCIONARIO", "FUZILEIRO", "UNIVERSITARIO", "VEREADOR", "VEREADORA", "VETERANO", "VICE", "VICE GOVERNADOR", "VICE PREFEITO", "VICE PRESIDENTE", "VICE REI", "VIGARIO", "VIGILANTE",
"VIRGEM", "VISCONDE", "VISCONDESSA", "VIUVA", "VIUVO", "VOLUNTARIA", "VOLUNTARIO", "VOVO", "GENERAL", "GENRO", "GOVERNADOR", "GOVERNADORA", "GRAO", "GRUMETE", "GUARDA", "GUIA", "HISTORIADOR", "HISTORIADORA", "IMACULADA", "IMACULADO",
"IMAME", "IMPERADOR", "IMPERATRIZ", "INDUSTRIAL", "INDUSTRIARIA", "INDUSTRIARIO", "INFANTA", "INFANTE", "INSPETOR", "INSPETORA", "INTENDENTE", "INTERVENTOR", "IRMA", "IRMAO", "IRMAOS", "JARDINEIRA", "JARDINEIRO", "JESUITA", "JORNALISTA",
"JUIZ", "JUIZ DE PAZ", "JUIZA", "JUNIOR", "JURISTA", "LANDGRAVE", "LANDGRAVINA", "LEGIONARIO", "LEILOEIRO", "LIBERTADOR", "LIVREIRO", "LOCUTOR", "LOCUTORA", "LORDE", "MADAME", "MADRE", "MAE", "MAESTRINA", "MAESTRO", "MAGISTRADO",
"MAJOR", "MAJOR BRIGADEIRO", "MAQUINISTA", "MARAJA", "MARANI", "MARCENEIRO", "MARECHAL", "MARINHEIRO", "MARITIMO", "MARQUES", "MARQUESA", "MARUJO", "MEDICA", "MEDICO", "MENINA", "MENINO", "MENORISTA", "MENORITA", "MESTRA",
"MESTRE", "METALURGICO", "MILITAR", "MINISTRA", "MINISTRO", "MISS", "MISSIONARIA", "MISSIONARIO", "MISTER", "MONGE", "MONJA", "MONSENHOR", "MOTORISTA", "MUSICO", "NATURALISTA", "NETA", "NETO", "NORA", "NOSSA", "NOSSA SENHORA",
"NOSSO", "NOSSO SENHOR", "NOVELISTA", "NOVICA", "NOVICO", "NUNCIO", "OFICIAL", "OPERARIA", "OPERARIO", "ORADOR", "ORADORA", "ORGANISTA", "OUTROS", "OUVIDOR", "PADRE", "PAI", "PAISAGISTA", "PAPA", "PAPISA", "PAROCO", "PARTEIRA",
"PASTOR", "PASTORA", "PATEIRO", "PESCADOR", "PESCADORA", "PILOTO", "PINTOR", "PINTORA", "PIO", "PIONEIRA", "PIONEIRO", "PITON", "PITONISA", "POETA", "POETISA", "POLICIAL", "PONTIFICE", "PRACA", "PRACINHA", "PREFEITA", "PREFEITO",
"PRELADA", "PRELADO", "PRESBITERO", "PRESIDENTA", "PRESIDENTE", "PRIMA", "PRIMO", "PRINCESA", "PRINCIPE", "PRIOR", "PRIORA", "PRIORESA", "PROCURADOR", "PROCURADORA", "PROFESSOR", "PROFESSOR DOUTOR", "PROFESSORA", "PROFETA", "PROFETISA",
"PROMOTOR", "PROMOTORA", "PROVEDOR", "PROVEDORA", "PUBLICITARIA", "PUBLICITARIO", "QUIMICA", "QUIMICO", "RABI", "RABINO", "RADIALISTA", "RAINHA", "RAJA", "RANI", "RECRUTA", "REGEDOR", "REGENTE", "REI", "REITOR", "REITORA", "REMADOR",
"REPORTER", "REVERENDO", "SACERDOTE", "SACERDOTISA", "SACRISTA", "SACRISTAO", "SAGRADA", "SAGRADO", "SAINT", "SAN", "SANTA", "SANTISSIMA", "SANTO", "SAO", "SARGENTO", "SECRETARIA", "SECRETARIO", "SEGUNDO SARGENTO", "SEGUNDO TENENTE",
"SEMINARISTA", "SENADOR", "SENADORA", "SENHOR", "SENHORA", "SENHORIA", "SENHORITA", "SERTANISTA", "SERVIDOR", "SEU", "SINDICALISTA", "SINHA", "SOBRINHA", "SOBRINHO", "SOCIOLOGA", "SOCIOLOGO", "SOGRA", "SOGRO", "SOLDADO", "SOROR",
"SUB OFICIAL", "SUB TENENTE", "SUBDIRETOR", "SUBDIRETORA", "SUBOFICIAL", "SUBTENENTE", "SULTANA", "SULTAO", "TABELIA", "TABELIAO", "TABELIOA", "TEATROLOGO", "TENENTE", "TENENTE AVIADOR", "TENENTE CORONEL", "TIA", "TIO", "TIPOGRAFO",
"TITIA", "TITIO", "TOPOGRAFO", "TROVADOR",""]
	#FIM LISTA DE TITULOS
	lista_complementos = ["ALA","ALAMEDA INTERNA","ANDAR","ANEXO","APARTAMENTO","ARMAZEM","AVENIDA INTERNA","BANCA","BARRACA","BARRACAO","BLOCO","BOX","CABINE","CAIS","CASA","CHACARA","CHALE","COBERTURA","COMODO","CONJUNTO",
	"DEPENDENCIA","DEPOSITO","EDIFICIO","ENTRADA","ESTANCIA","FAZENDA","FNS","FRENTE","FUNDOS","GALERIA","GARAGEM","GRANJA","GRUPO","GUICHE","HABITACAO","HANGAR","LADO","LAJE","LOJA","LOTE","MANSAO","MODULO","OUTROS","PAVILHAO",
	"PAVIMENTO","PECA","PORAO","PORTA","PORTAO","PREDIO","QUADRA","QUARTO","QUINTA","QUITINETE","RUA INTERNA","SALA","SEDE","SITIO","SOBRADO","SOBRELOJA","SUBSOLO","SUCAM","SUITE","TERREO","TRAVESSA INTERNA",""]
	#FIM LISTA COMPLEMENTOS
	
	if "GET" == request.method:
		return render(request, "upload_csv.html", data)
		
	csv_file = request.FILES['file']
	
	if ( not csv_file.name.endswith('.csv')):
		messages.error(request, 'ARQUIVO INVÁLIDO')
		return redirect ( 'upload_csv')
		

	# elif csv.Sniffer().has_header(csv_file.read().decode("utf-8")) == True:
		# messages.error(request, 'FAVOR RETIRAR CABEÇALHO DO ARQUIVO CSV')
		# return redirect ('upload_csv')
		
	else:
		data_set = csv_file.read().decode("utf-8")
		
		
		
		io_string = io.StringIO(data_set)
		
	
		#next(io_string)	
		
		linhas = csv.reader(io_string, delimiter=';', lineterminator='\n')
		
		
		
		for column in linhas:
			if (column[0] == ''):
				messages.error(request, 'CAMPO CÓDIGO SETOR  EM BRANCO LINHA  {}'.format(linhas.line_num))
				return redirect ('upload_csv')
				
			elif len(column[0]) != 15:
				messages.info(request, 'TAMANHO CAMPO CÓDIGO SETOR INVÁLIDO LINHA {} VALOR:  {}'.format(linhas.line_num,column[0]))
				return redirect ('upload_csv')
				
			elif column[0].isnumeric() == False:
				messages.error(request, 'CAMPO CÓDIGO SETOR NÃO NUMÉRICO LINHA {} VALOR:  {}'.format(linhas.line_num,column[0]))
				return redirect ('upload_csv')
				#FIM VALIDAÇÃO COD_SETOR
				
			elif (column[1] == '' or column[1].isspace() == True):
				messages.error(request, 'CAMPO TIPO EM BRANCO LINHA {}'.format(linhas.line_num))
				return redirect ('upload_csv')	
				
			# elif ( len(column[1]) > 30):
				# messages.info(request, 'TAMANHO CAMPO TIPO INVÁLIDO LINHA {} VALOR: {}'.format(linhas.line_num,column[1]))
				# return redirect ('upload_csv')
				
			
			elif (column[1].islower() ):
				messages.info(request, 'CAMPO TIPO DEVE SER MAIÚSCULO LINHA {} VALOR: {}'.format(linhas.line_num,column[1]))
				return redirect ('upload_csv')
			
			elif (column[1].strip() not in lista_tipos):
				messages.info(request, 'CAMPO TIPO INVÁLIDO LINHA {} VALOR: {}'.format(linhas.line_num,column[1]))
				return redirect ('upload_csv')
			
			
				#FIM VALIDAÇÃO CAMPO TIPO
				
			# elif (len(column[2]) > 30 ):
				# messages.info(request, 'TAMANHO CAMPO TÍTULO INVÁLIDO LINHA {} VALOR: {}'.format(linhas.line_num,column[2]))
				# return redirect ('upload_csv')	
				
			elif (column[2].islower() ):
				messages.info(request, 'CAMPO TÍTULO DEVE SER MAIÚSCULO LINHA {} VALOR: {}'.format(linhas.line_num,column[2]))
				return redirect ('upload_csv')
			
			elif( column[2].isnumeric()):
				messages.info(request, 'TÍTULO INVÁLIDO LINHA {} VALOR: {}'.format(linhas.line_num,column[2]))
				return redirect ('upload_csv')
		
			# elif ( column[2].isalpha() and column[2].strip() not in lista_titulos   ):
				 # messages.info(request, 'TÍTULO INVÁLIDO LINHA {} VALOR: {}'.format(linhas.line_num,column[2]))
				 # return redirect ('upload_csv')
			
			elif ( column[2].isspace() == False  and column[2].strip() not in lista_titulos   ):
				 messages.info(request, 'TÍTULO INVÁLIDO porra LINHA {} VALOR: {}'.format(linhas.line_num,column[2]))
				 return redirect ('upload_csv')
			
					#FIM VALIDAÇÃO CAMPO TITULO
				
				
			elif ( column[3] == '' or column[3].isspace() == True):
				messages.error(request, 'CAMPO NOME SEGUIMENTO LOGRADOURO EM BRANCO LINHA {}'.format(linhas.line_num))
				return redirect ('upload_csv')

			elif (len(column[3]) > 60 ):
				messages.info(request, ' TAMANHO CAMPO NOME SEGUIMENTO LOGRADOURO INVÁLIDO LINHA {} VALOR: {}'.format(linhas.line_num,column[3]))
				return redirect ('upload_csv')
			
			elif (column[3].islower() ):
				messages.info(request, 'CAMPO NOME SEGUIMENTO LOGRADOURO DEVE SER MAIÚSCULO LINHA {} VALOR: {}'.format(linhas.line_num,column[3]))
				return redirect ('upload_csv')
				#FIM VALIDAÇÃO CAMPO seglogr
				
			elif (column[4] == '' or column[4].isspace() == True):
				messages.error(request, 'CAMPO CÓDIGO QUADRA EM BRANCO LINHA {}'.format(linhas.line_num))
				return redirect ('upload_csv')
				
			elif (len(column[4]) > 3 ):
				messages.info(request, 'TAMANHO CAMPO CÓDIGO QUADRA INVÁLIDO LINHA {} VALOR: {}'.format(linhas.line_num,column[4]))
				return redirect ('upload_csv')
				
				
			elif (column[4].isnumeric() == False):
				messages.error(request, 'CAMPO CÓDIGO QUADRA NÃO NUMÉRICO LINHA {} VALOR: {}'.format(linhas.line_num,column[4]))
				return redirect ('upload_csv')
				#FIM VALIDAÇÃO COD_QUADRA
				
				
			elif column[5] == '' or column[5].isspace() == True:
				messages.error(request, 'CAMPO CÓDIGO FACE EM BRANCO LINHA {}'.format(linhas.line_num))
				return redirect ('upload_csv')

			
			elif (len(column[5]) > 3 ):
				messages.info(request, ' TAMANHO CAMPO CÓDIGO FACE INVÁLIDO LINHA {} VALOR: {}'.format(linhas.line_num,column[5]))
				return redirect ('upload_csv')
			
			elif (column[5].isnumeric() == False):
				messages.error(request, 'CAMPO CÓDIGO FACE NÃO NUMÉRICO LINHA {} VALOR: {}'.format(linhas.line_num,column[5]))
				return redirect ('upload_csv')
				#FIM VALIDAÇÃO COD_FACE
			
			elif column[6].isnumeric() == False:
				messages.error(request, 'CAMPO NÚMERO ENDEREÇO NÃO NUMÉRICO LINHA {} VALOR:  {}'.format(linhas.line_num,column[6]))
				return redirect ('upload_csv')
				
			elif (len(column[6]) > 10 ):
				messages.info(request, 'TAMANHO CAMPO NÚMERO ENDEREÇO INVÁLIDO LINHA {}  VALOR: {}'.format(linhas.line_num,column[6]))
				return redirect ('upload_csv')
				#FIM VALIDAÇÃO COD_ENDEREÇO
				
				
			elif (len(column[7]) > 7 ):
				messages.info(request, 'TAMANHO CAMPO MODIFICADOR INVÁLIDO LINHA {} VALOR: {}'.format(linhas.line_num,column[7]))
				return redirect ('upload_csv')
				#FIM VALIDAÇÃO MODIFICADOR	
				
			elif (column[8].islower() ):
				messages.info(request, 'CAMPO COMPLEMENTO DEVE SER MAIÚSCULO LINHA {} VALOR: {}'.format(linhas.line_num,column[8]))
				return redirect ('upload_csv')
			
		
			elif (column[8].isnumeric() ):
				messages.info(request, 'CAMPO COMPLEMENTO 1 INVÁLIDO LINHA {} VALOR: {}'.format(linhas.line_num,column[8]))
				return redirect ('upload_csv')
				
			# elif ( column[8].isalpha()== True and column[8].strip() not in lista_complementos  ):
				# messages.info(request, 'CAMPO COMPLEMENTO 1 INVÁLIDO LINHA {} VALOR: {}'.format(linhas.line_num,column[8]))
				# return redirect ('upload_csv')
	
			elif ( column[8].isspace()== False and column[8].strip() not in lista_complementos  ):
				messages.info(request, 'CAMPO COMPLEMENTO 1 INVÁLIDO LINHA {} VALOR: {}'.format(linhas.line_num,column[8]))
				return redirect ('upload_csv')
				#FIM VALIDAÇÃO COMPLEMENTO 1	
			
			elif (len(column[9]) > 10 ):
				messages.info(request, ' TAMANHO CAMPO VALOR 1 INVÁLIDO LINHA {} VALOR : {}'.format(linhas.line_num,column[9]))
				return redirect ('upload_csv')
			elif(column[8] == '' and column[9]):
					messages.info(request, ' PREENCHA O CAMPO COMPLEMENTO 1 LINHA {} VALOR: {}'.format(linhas.line_num,column[9]))
					return redirect ('upload_csv')
			
		
			
				
				#FIM VALIDAÇÃO VALOR 1	
			
			elif ( column[10].isnumeric()):
				messages.info(request, ' CAMPO COMPLEMENTO 2 INVÁLIDO LINHA {} VALOR: {}'.format(linhas.line_num,column[10]))
				return redirect ('upload_csv')
				
			elif (column[10].islower() ):
				messages.info(request, 'CAMPO COMPLEMENTO DEVE SER MAIÚSCULO LINHA {} VALOR: {}'.format(linhas.line_num,column[10]))
				return redirect ('upload_csv') 
				
			# elif(  column[10].isalpha()== True and column[10] not in lista_complementos):
					# messages.info(request, ' CAMPO COMPLEMENTO 2 INVÁLIDO LINHA {} VALOR: {}'.format(linhas.line_num,column[10]))
					# return redirect ('upload_csv')
			elif(  column[10].isspace()== False and column[10] not in lista_complementos):
					messages.info(request, ' CAMPO COMPLEMENTO 2 INVÁLIDO LINHA {} VALOR: {}'.format(linhas.line_num,column[10]))
					return redirect ('upload_csv')
			elif ( column[8] == '' and column[10]):
				messages.info(request, ' PREENCHA PRIMEIRO O CAMPO COMPLEMENTO 1 LINHA {} VALOR: {}'.format(linhas.line_num,column[10]))
				return redirect ('upload_csv')
				#FIM VALIDAÇÃO COMPLEMENTO 2
				
			elif (len(column[11]) > 10 ):
				messages.info(request, 'TAMANHO CAMPO VALOR 2 INVÁLIDO LINHA {} : {}'.format(linhas.line_num,column[11]))
				return redirect ('upload_csv')
				
			elif(column[10] == '' and column[11]):
					messages.info(request, ' PREENCHA CAMPO COMPLEMENTO 2 LINHA {} VALOR: {}'.format(linhas.line_num,column[11]))
					return redirect ('upload_csv')
					
		
				#FIM VALIDAÇÃO VALOR 2
			
			elif ( column[12].isnumeric() ):
				messages.info(request, 'CAMPO COMPLEMENTO 3 INVÁLIDO LINHA {} VALOR: {}'.format(linhas.line_num,column[12]))
				return redirect ('upload_csv')
				
			elif ( column[12].islower() ):
				messages.info(request, 'CAMPO COMPLEMENTO DEVE SER MAIÚSCULO LINHA {} VALOR: {}'.format(linhas.line_num,column[12]))
				return redirect ('upload_csv')
			# elif ( column[12].isalpha()== True and column[12] not in lista_complementos ):
				# messages.info(request, 'CAMPO COMPLEMENTO 3 INVÁLIDO LINHA {} VALOR: {}'.format(linhas.line_num,column[12]))
				# return redirect ('upload_csv')
			elif ( column[12].isspace()== False and column[12] not in lista_complementos ):
				messages.info(request, 'CAMPO COMPLEMENTO 3 INVÁLIDO LINHA {} VALOR: {}'.format(linhas.line_num,column[12]))
				return redirect ('upload_csv')
			
			elif ( column[10] == '' and column[12]):
				messages.info(request, ' PREENCHA PRIMEIRO O COMPLEMENTO 2 LINHA {} VALOR: {}'.format(linhas.line_num,column[12]))
				return redirect ('upload_csv')
			
		
				#FIM VALIDAÇÃO COMPLEMENTO 3
				
				
			elif (len(column[13]) > 10 ):
				messages.info(request, 'TAMANHO CAMPO VALOR 3 INVÁLIDO LINHA {} VALOR: {}'.format(linhas.line_num,column[13]))
				return redirect ('upload_csv')
			elif(column[12] == '' and column[13]):
					messages.info(request, ' PREENCHA CAMPO COMPLEMENTO 3 LINHA {} VALOR: {}'.format(linhas.line_num,column[13]))
					return redirect ('upload_csv')
		
				#FIM VALIDAÇÃO VALOR 3	
			
			elif ( column[14].isnumeric()):
				messages.info(request, 'CAMPO COMPLEMENTO 4 INVÁLIDO LINHA {} VALOR: {}'.format(linhas.line_num,column[14]))
				return redirect ('upload_csv')
			elif ( column[14].islower()  ):
				messages.info(request, 'CAMPO COMPLEMENTO DEVE SER MAIÚSCULO LINHA {} VALOR: {}'.format(linhas.line_num,column[14]))
				return redirect ('upload_csv')
			# elif ( column[14].isalpha()== True and column[14] not in lista_complementos ):
				# messages.info(request, 'CAMPO COMPLEMENTO 4 INVÁLIDO LINHA {} VALOR: {}'.format(linhas.line_num,column[14]))
				# return redirect ('upload_csv')
			elif ( column[14].isspace()== False and column[14] not in lista_complementos ):
				messages.info(request, 'CAMPO COMPLEMENTO 4 INVÁLIDO LINHA {} VALOR: {}'.format(linhas.line_num,column[14]))
				return redirect ('upload_csv')
			elif ( column[12] == '' and column[14]):
				messages.info(request, ' PREENCHA PRIMEIRO O COMPLEMENTO 3 LINHA {} VALOR: {}'.format(linhas.line_num,column[14]))
				return redirect ('upload_csv')
					
			
				#FIM VALIDAÇÃO COMPLEMENTO 4
				
				
			elif (len(column[15]) > 10 ):
				messages.info(request, 'TAMANHO CAMPO VALOR 4 INVÁLIDO LINHA {} : {}'.format(linhas.line_num,column[15]))
				return redirect ('upload_csv')
				
			elif(column[14] == '' and column[15]):
					messages.info(request, ' PREENCHA CAMPO COMPLEMENTO 4 LINHA {} VALOR: {}'.format(linhas.line_num,column[15]))
					return redirect ('upload_csv')
		
				#FIM VALIDAÇÃO VALOR 4
				
				
				
			elif ( column[16].isnumeric() ):
				messages.info(request, 'CAMPO COMPLEMENTO 5 INVÁLIDO LINHA {} VALOR: {}'.format(linhas.line_num,column[16]))
				return redirect ('upload_csv')	
			
			elif ( column[16].islower()		):
				messages.info(request, 'CAMPO COMPLEMENTO DEVE SER MAIÚSCULO LINHA {} VALOR: {}'.format(linhas.line_num,column[16]))
				return redirect ('upload_csv')	
			
			# elif ( column[16].isalpha()== True and column[16].strip() not in lista_complementos ):
				# messages.info(request, 'CAMPO COMPLEMENTO 5 INVÁLIDO LINHA {} VALOR: {}'.format(linhas.line_num,column[16]))
				# return redirect ('upload_csv')
					
			elif ( column[16].isspace()== False and column[16].strip() not in lista_complementos ):
				messages.info(request, 'CAMPO COMPLEMENTO 5 INVÁLIDO LINHA {} VALOR: {}'.format(linhas.line_num,column[16]))
				return redirect ('upload_csv')
	
			elif ( column[14] == '' and column[16]):
				messages.info(request, ' PREENCHA PRIMEIRO O COMPLEMENTO 4 LINHA {} VALOR: {}'.format(linhas.line_num,column[16]))
				return redirect ('upload_csv')
		
				#FIM VALIDAÇÃO COMPLEMENTO 5
				
			elif (len(column[17]) > 10 ):
				messages.info(request, 'TAMANHO CAMPO VALOR 5 INVÁLIDO LINHA {} : {}'.format(linhas.line_num,column[17]))
				return redirect ('upload_csv')
			elif(column[16] == '' and column[17]):
					messages.info(request, ' PREENCHA CAMPO COMPLEMENTO 5 LINHA {} VALOR: {}'.format(linhas.line_num,column[17]))
					return redirect ('upload_csv')
		
				#FIM VALIDAÇÃO VALOR 5
				
				
				
			elif (column[18] not in  ['12', '13']):
				messages.success(request, 'CAMPO CÓDIGO ESPÉCIE INVÁLIDO LINHA {} VALOR: {}'.format(linhas.line_num,column[18]))
				return redirect ('upload_csv')
				
				
				
			else:
			
				check += t_face_cnefe.objects.filter(
				COD_SETOR = column[0],
				NUM_QUADRA = column[4],
				NUM_FACE = column[5]
				)
				total +=  t_face_cnefe.objects.filter(COD_SETOR = column[0],
				NUM_QUADRA = column[4],
				NUM_FACE = column[5]).count()
		
		
	
		return render(request, 'index2.html', {'check': check, 'total':total})	
			