from app.config.connection import db
from sqlalchemy import text

class MarcaDAO:
    @staticmethod
    def crear_marca(marca):
        try:
            query = text("CALL usp_nuevaMarca(:p_marca)")
            db.session.execute(query, {
                'p_marca': marca
            })
            
            id_marca = db.session.execute(text("SELECT LAST_INSERT_ID()")).fetchone()[0]
            db.session.commit()
            return id_marca
            
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al crear marca: {str(e)}")
    
    @staticmethod
    def listar_marcas():
        try:
            query = text("CALL usp_listarMarcas()")
            result = db.session.execute(query)
            
            marcas = []
            for row in result:
                marcas.append({
                    'idMarca': row[0],
                    'marca': row[1]
                })
            
            return marcas
            
        except Exception as e:
            raise Exception(f"Error al listar marcas: {str(e)}")
    
    @staticmethod
    def obtener_marca_por_id(id_marca):
        try:
            query = text("CALL usp_obtenerInfoDeMarcaPorId(:p_idMarca)")
            result = db.session.execute(query, {'p_idMarca': id_marca})
            row = result.fetchone()
            
            if row:
                return {
                    'idMarca': row[0],
                    'marca': row[1]
                }
            return None
            
        except Exception as e:
            raise Exception(f"Error al obtener información de la marca: {str(e)}")
    
    @staticmethod
    def obtener_id_marca_por_nombre(marca):
        try:
            query = text("CALL usp_obtenerIdMarcaPorNombre(:p_marca)")
            result = db.session.execute(query, {'p_marca': marca})
            row = result.fetchone()
            
            if row:
                return row[0]
            return None
            
        except Exception as e:
            raise Exception(f"Error al obtener ID de marca por nombre: {str(e)}")
    
    @staticmethod
    def contar_marca_por_nombre(marca):
        try:
            query = text("CALL usp_contarMarcaPorNombre(:p_marca)")
            result = db.session.execute(query, {'p_marca': marca})
            row = result.fetchone()
            
            return row[0] if row else 0
            
        except Exception as e:
            raise Exception(f"Error al contar marca por nombre: {str(e)}")