-- ARCHIVO DE DATOS INICIALES
-- MARCAS
insert into Marca (marca) values
('Gloria'),       
('Laive'),       
('Primor'),       
('San Fernando'), 
('Florida'),      
('Costeño'),     
('Don Vittorio'), 
('Alicorp'),     
('Fanny'),        
('Natura');      

-- CATEGORIAS
insert into Categoria (categoria) values
('Lácteos'),
('Conservas'),
('Fideos'),
('Arroz'),
('Azúcar'),
('Aceites'),
('Carnes'),
('Embutidos'),
('Pastas'),
('Bebidas'),
('Galletas'),
('Snacks'),
('Cereales'),
('Limpieza'),
('Higiene personal'),
('Panadería'),
('Salsas'),
('Legumbres'),
('Congelados'),
('Frutas y Verduras');

-- PRODUCTOS
insert into Producto (idCategoria, nombreProducto, descripcion, idMarca, precio, valoracion, imagen) values
(31, 'Leche UHT', 'Deslactosada', 92, 4.50, 9, 'https://dojiw2m9tvv09.cloudfront.net/75518/product/08821995657.png'),
(31, 'Leche Entera', 'Fresca', 93, 4.20, 8, 'https://oechsle.vteximg.com.br/arquivos/ids/1856174-1000-1000/image-35c98251e4e048668dd2581908dedefb.jpg?v=637495318115200000'),
(32, 'Atún en Aceite', 'Lomo', 96, 6.80, 7, 'https://www.fullabarrotes.com/wp-content/uploads/2020/03/trozo_atun_aceite_vegetal_fanny_170g.jpg'),
(32, 'Atún Light', 'Bajo sodio', 95, 6.50, 8, 'https://prueba.webfacel.com/assets/uploads/989b13e56b985217aee7bfb191f89e5c.jpg'),
(33, 'Fideos Spaghetti', 'Gruesos', 98, 3.20, 9, 'https://metroio.vtexassets.com/arquivos/ids/306072/Pastinas-Codo-Rayado-Alianza-Bolsa-250-g-2-148265.jpg?v=638179482959470000'),
(33, 'Fideos Tallarín', 'Delgado', 97, 3.50, 10, 'https://metroio.vtexassets.com/arquivos/ids/405515-800-auto?v=638181138612730000&width=800&height=auto&aspect=true'),
(34, 'Arroz Superior', 'Extra', 94, 3.80, 9, 'https://d29d6yxlntu8gw.cloudfront.net/wp-content/uploads/2024/11/ARR0415.png'),
(34, 'Arroz Costeño', 'Grado 1', 96, 3.70, 8, 'https://plazavea.vteximg.com.br/arquivos/ids/27552446-418-418/433778.jpg'),
(35, 'Azúcar Rubia', 'Empacada', 96, 2.90, 7, 'https://costenoalimentos.com.pe/media/1581/akEVmVSuaOkrzbGlrk6JhmtwRQPg1fXkueJSnMeQ.jpg'),
(36, 'Aceite Vegetal', 'Clásico', 94, 7.20, 9, 'https://realplaza.vtexassets.com/arquivos/ids/29304470/image-7f73fe6652cd4186b77b1bf89faf41df.jpg?v=637925977035200000'),
(36, 'Aceite Girasol', 'Ligero', 101, 8.00, 8, 'https://www.stock.com.py/images/thumbs/0195408.jpeg'),
(37, 'Pechuga de Pollo', 'Congelada', 95, 15.50, 9, 'https://metroio.vtexassets.com/arquivos/ids/456392/Pechuga-de-Pollo-con-Alas-Congelada-San-Fernando-x-kg-1-351645421.jpg?v=638285692053570000'),
(38, 'Hot Dog Pack', 'Clásico', 93, 8.90, 8, 'https://storage.googleapis.com/web-laive-storage/Media/pages/hotdog-suizo-suiza-120.jpg'),
(39, 'Lasaña Lista', 'Congelada', 97, 12.00, 7, 'https://miamarket.pe/assets/uploads/850d38df254426fe24bbaeb86b176d6a.jpg'),
(40, 'Jugo de Naranja', 'Sin azúcar', 92, 4.50, 6, 'https://plazavea.vteximg.com.br/arquivos/ids/27597217-450-450/20075685.jpg?v=638320896288370000');



