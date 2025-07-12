from app.config.connection import db
from sqlalchemy import text

class VendedorDAO:
    @staticmethod
    def crear_vendedor(vendedor, valoracion):
        try:
            query = text("CALL usp_nuevoVendedor(:p_vendedor, :p_valoracion)")
            db.session.execute(query, {
                'p_vendedor': vendedor,
                'p_valoracion': valoracion
            })
            
            id_vendedor = db.session.execute(text("SELECT LAST_INSERT_ID()")).fetchone()[0]
            db.session.commit()
            return id_vendedor
            
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al crear vendedor: {str(e)}")
    
    @staticmethod
    def crear_relacion_usuario_establecimiento(id_vendedor, id_establecimiento, id_usuario):
        try:
            query = text("CALL usp_nuevoUsuarioEstablecimiento(:p_idVendedor, :p_idEstablecimiento, :p_idUsuario)")
            db.session.execute(query, {
                'p_idVendedor': id_vendedor,
                'p_idEstablecimiento': id_establecimiento,
                'p_idUsuario': id_usuario
            })
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al crear relación usuario-establecimiento: {str(e)}")
    
    @staticmethod
    def listar_vendedores_por_usuario(id_usuario):
        try:
            query = text("CALL usp_listarVendedoresDeUsuario(:p_idUsuario)")
            result = db.session.execute(query, {'p_idUsuario': id_usuario})
            
            vendedores = []
            for row in result:
                vendedores.append({
                    'idVendedor': row[0],
                    'vendedor': row[1],
                    'valoracion': row[2]
                })
            
            return vendedores
            
        except Exception as e:
            raise Exception(f"Error al listar vendedores de usuario: {str(e)}")
    
    @staticmethod
    def obtener_vendedor_por_id(id_vendedor):
        try:
            query = text("CALL usp_obtenerInfoDeVendedorPorId(:p_idVendedor)")
            result = db.session.execute(query, {'p_idVendedor': id_vendedor})
            row = result.fetchone()
            
            if row:
                return {
                    'idVendedor': row[0],
                    'vendedor': row[1],
                    'valoracion': row[2]
                }
            return None
            
        except Exception as e:
            raise Exception(f"Error al obtener información del vendedor: {str(e)}")
    
    @staticmethod
    def verificar_vendedor_en_establecimiento(id_vendedor, id_establecimiento):
        try:
            query = text("""
                SELECT COUNT(*) FROM UsuarioEstablecimiento 
                WHERE idVendedor = :p_idVendedor AND idEstablecimiento = :p_idEstablecimiento
            """)
            result = db.session.execute(query, {
                'p_idVendedor': id_vendedor,
                'p_idEstablecimiento': id_establecimiento
            })
            count = result.fetchone()[0]
            return count > 0
            
        except Exception as e:
            raise Exception(f"Error al verificar vendedor en establecimiento: {str(e)}")