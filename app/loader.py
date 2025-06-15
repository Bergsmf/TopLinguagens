from classes.vagas import Vagas


def salva_vagas():
    vagas = Vagas()
    vagas.obtem_vagas()
    vagas.dump_vagas()

if __name__ == "__main__":
    salva_vagas()
