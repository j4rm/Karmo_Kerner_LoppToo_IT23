import json
from datetime import datetime


class Andmetöötleja:
    def __init__(self, faili_tee):
        with open(faili_tee, 'r', encoding='utf-8') as file:
            self.andmed = json.load(file)
        self.tanane_kuupäev = datetime.today()
        self.statistika = self.arvuta_statistika()

    def arvuta_vanus(self, sünniaeg, surmaaeg=None):
        if not sünniaeg:
            return 0
        sünniaeg = datetime.strptime(sünniaeg, "%Y-%m-%d")
        if not surmaaeg or surmaaeg == "0000-00-00":
            return (self.tanane_kuupäev - sünniaeg).days // 365
        else:
            surmaaeg = datetime.strptime(surmaaeg, "%Y-%m-%d")
            return (surmaaeg - sünniaeg).days // 365

    def arvuta_statistika(self):
        isikute_arv = 0
        pikim_nimi = ""
        pikim_nimi_pikkus = 0
        vanim_elus_nimi = ""
        vanim_elus_vanus = 0
        vanim_elus_sünniaeg = ""
        vanim_surnud_nimi = ""
        vanim_surnud_vanus = 0
        vanim_surnud_sünniaeg = ""
        vanim_surnud_surmaaeg = ""
        näitlejate_arv = 0
        sündinud_1997 = 0
        elukutsete_hulk = set()
        rohkem_kui_kaks_nime = 0
        sama_sünni_surmaaeg = 0
        elus_arv = 0
        surnud_arv = 0

        for isik in self.andmed:
            isikute_arv += 1

            # Pikim nimi
            nimi_pikkus = len(isik["nimi"].replace(" ", ""))
            if nimi_pikkus > pikim_nimi_pikkus:
                pikim_nimi = isik["nimi"]
                pikim_nimi_pikkus = nimi_pikkus

            # Vanus
            sünniaeg = isik.get("sundinud")
            surmaaeg = isik.get("surnud", "0000-00-00")
            vanus = self.arvuta_vanus(sünniaeg, surmaaeg)

            # Vanim elus
            if surmaaeg == "0000-00-00":
                elus_arv += 1
                if vanus > vanim_elus_vanus:
                    vanim_elus_nimi = isik["nimi"]
                    vanim_elus_vanus = vanus
                    vanim_elus_sünniaeg = sünniaeg
            else:
                surnud_arv += 1
                if vanus > vanim_surnud_vanus:
                    vanim_surnud_nimi = isik["nimi"]
                    vanim_surnud_vanus = vanus
                    vanim_surnud_sünniaeg = sünniaeg
                    vanim_surnud_surmaaeg = surmaaeg

            # Näitlejad
            if "näitleja" in isik["amet"].lower():
                näitlejate_arv += 1

            # Sündinud 1997
            if sünniaeg and sünniaeg.startswith("1997"):
                sündinud_1997 += 1

            # Elukutsed
            elukutsete_hulk.add(isik["amet"])

            # Rohkem kui kaks nime
            if len(isik["nimi"].split(' ')) > 2:
                rohkem_kui_kaks_nime += 1

            # Sünniaeg ja surmaaeg sama kuu ja päev
            if surmaaeg != "0000-00-00" and sünniaeg and sünniaeg[5:] == surmaaeg[5:]:
                sama_sünni_surmaaeg += 1

        return {
            "isikute_arv": isikute_arv,
            "pikim_nimi": (pikim_nimi, pikim_nimi_pikkus),
            "vanim_elus_isik": (vanim_elus_nimi, vanim_elus_vanus, vanim_elus_sünniaeg),
            "vanim_surnud_isik": (vanim_surnud_nimi, vanim_surnud_vanus, vanim_surnud_sünniaeg, vanim_surnud_surmaaeg),
            "näitlejate_arv": näitlejate_arv,
            "sündinud_1997": sündinud_1997,
            "erinevad_elukutsed": len(elukutsete_hulk),
            "rohkem_kui_kaks_nime": rohkem_kui_kaks_nime,
            "sama_sünni_surmaaeg": sama_sünni_surmaaeg,
            "elus_arv": elus_arv,
            "surnud_arv": surnud_arv,
        }

    def isikute_arv(self):
        return self.statistika["isikute_arv"]

    def kõige_pikem_nimi(self):
        return self.statistika["pikim_nimi"]

    def vanim_elus_isik(self):
        nimi, vanus, sünniaeg = self.statistika["vanim_elus_isik"]
        sünnikuupäev = datetime.strptime(sünniaeg, "%Y-%m-%d").strftime("%d.%m.%Y")
        return f"{nimi}, Vanus: {vanus}, Sündis: {sünnikuupäev}"

    def vanim_surnud_isik(self):
        nimi, vanus, sünniaeg, surmaaeg = self.statistika["vanim_surnud_isik"]
        sünnikuupäev = datetime.strptime(sünniaeg, "%Y-%m-%d").strftime("%d.%m.%Y")
        surmakuupäev = datetime.strptime(surmaaeg, "%Y-%m-%d").strftime("%d.%m.%Y")
        return f"{nimi}, Vanus: {vanus}, Sündis: {sünnikuupäev}, Suri: {surmakuupäev}"

    def näitlejate_arv(self):
        return self.statistika["näitlejate_arv"]

    def sündinud_1997(self):
        return self.statistika["sündinud_1997"]

    def erinevad_elukutsed(self):
        return self.statistika["erinevad_elukutsed"]

    def rohkem_kui_kaks_nime(self):
        return self.statistika["rohkem_kui_kaks_nime"]

    def sama_sünni_surmaaeg(self):
        return self.statistika["sama_sünni_surmaaeg"]

    def elavate_ja_surnute_arv(self):
        return self.statistika["elus_arv"], self.statistika["surnud_arv"]
