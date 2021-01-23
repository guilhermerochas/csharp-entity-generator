import pyodbc
import os
from data_types import DataTypes
from pathlib import Path
from sys import argv


def capitalizeString(val: str) -> str:
    return ''.join([letter[0].upper() + letter[1:] for letter in val.split()])


class EntityGenerator():
    def __init__(self, conn_file: str):
        conn = pyodbc.connect(conn_file)
        self.query = conn.cursor()

    def gen_entity(self, table_name: str) -> str:
        try:
            self.table_name = table_name
            entity = self.query.execute(f'exec sp_help {table_name}')
            entity.nextset()

            values = []

            for row in entity:
                values.append([row[0], row[1], row[3], row[6], 'no'])

            for _ in range(4):
                entity.nextset()

            for row in entity:
                primary_keys = [key.strip() for key in row[-1].split(',')]
                for key in primary_keys:
                    for val in values:
                        if key == val[0]:
                            val[-1] = 'yes'

            entity_string = """
                [Table("{tb}")]
                public virtual {name} 
                {{""".format(tb=table_name,
                             name=str(table_name.replace('_', '')))

            for field in values:
                column = """
                    {is_key}
                    [Column("{col_name}")]
                    public {col_type}{nullable} {field_name} {{ get; set; }}
                """.format(is_key='[Key]' if field[-1] == 'yes' else '',
                           col_name=field[0],
                           nullable='?' if
                           (field[3] == 'yes'
                            and DataTypes[field[1]].value != 'string') else '',
                           col_type=DataTypes[field[1]].value,
                           field_name=capitalizeString(field[0].replace(
                               '_', '')))
                entity_string += column

            entity_string += """}"""

            return entity_string
        except:
            print(f'Não foi possivel gerar a tabela')
            return None

    def save_file(self, gen_value: str) -> bool:
        path = os.path.join(os.path.expanduser('~'), 'Desktop',
                            f'{self.table_name}.cs')

        if not os.path.isfile(path):
            Path(path).touch()

        with open(path, 'a') as file:
            file.write(gen_value)


def main() -> None:
    if (len(argv) < 2):
        print('passe o nome da tabela como parametro!')
        return

    file = ''
    with open('./db_file.txt', 'r') as f:
        file = f.read()

    eg = EntityGenerator(file)
    gen_val = eg.gen_entity(str(argv[1]))

    if (gen_val is None):
        print('Não foi possivel gerar a entidade')
        return

    eg.save_file(gen_val)


if __name__ == "__main__":
    main()
