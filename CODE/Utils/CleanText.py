from TextCleaner import TextCleaner

Codigo_Civil = TextCleaner("C:/Users/diogo/Desktop/perkier tech/ARAG/ARAG/artifacts/CODIGO_CIVIL_RAW.txt")
Codigo_Civil.clean_txt("CIVIL")
Codigo_Civil.create_json_data()
Codigo_Civil.save_json_data("codigo_civil")

Codigo_Penal = TextCleaner("C:/Users/diogo/Desktop/perkier tech/ARAG/ARAG/artifacts/CODIGO_PENAL_RAW.txt")
Codigo_Penal.clean_txt("PENAL")
Codigo_Penal.create_json_data()
Codigo_Penal.save_json_data("codigo_penal")