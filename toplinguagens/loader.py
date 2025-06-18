from classes.vagas import Vagas

if __name__ == '__main__':
    vagas = Vagas()
    vagas.obtem_vagas()
    vagas.dump_vagas()
    vagas.organiza_vagas()
    vagas.organiza_tecnologias()
    vagas.organiza_locais()
