import csv
import pathlib

test_name = ['blank']
test_vec = [0 for _ in range(24)]

# TODO: Usar pandas para el manejo del dataframe
class EmotionDataManagement:
    def __init__(self):
        self.emotion_data_dir = pathlib.Path(__file__).parent.parent / 'data'
        self.emotion_data_file = self.emotion_data_dir / 'emotion_data.csv'
        self.columns = [
            "emotion_name",
            "lps",
            "letl_a", "letl_b", "letl_c",
            "lebl_a", "lebl_b", "lebl_c",
            "rps",
            "retl_a", "retl_b", "retl_c",
            "rebl_a", "rebl_b", "rebl_c",
            "tl_a", "tl_b", "tl_c", "tl_d", "tl_e",
            "bl_a", "bl_b", "bl_c", "bl_d", "bl_e"
        ]

    def create_csv(self):
        # Crear un archivo CSV vacío con las columnas especificadas
        with open(self.emotion_data_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Escribir las columnas como el encabezado del archivo CSV
            writer.writerow(self.columns)

    def add_row(self, emotion_name=test_name, data=test_vec):
        with open(self.emotion_data_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(emotion_name + data)




if __name__ == '__main__':
    emotion_data_management = EmotionDataManagement()
    emotion_data_management.create_csv()
    emotion_data_management.add_row()
