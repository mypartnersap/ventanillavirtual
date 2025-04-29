*MODIFICACIÓN AL MODELO
   1) Expansión del modelo User con el modelo UserProfile que permite añadir la información de teléfono, identifiacion y tipo de identificacion
   2) Se implementó un nuevo modelo para guarder los registros de los usuarios (RecordLoggedModel) que se asocia con el modelo User
   3) Se implementó guardar el archivo que suba el usuario en el directorio "media/file_system" en vez de guardar el archivo en base 64 en la base de datos.
   4) El modelo inicial no está funcional, se dejó para comparación.


*SE DEJÓ FUNCIONANDO EL SISTEMA DE LOGGEO DE USUARIO
    1) Los usuarios se deben crear por shell o por panel del super usuario.
    2) Registro de ususario no implementado.
    3) El legin de ususarios es con username y contraseña.
    4) Cuando se crea un usuario, se debe editar el perfil de este usuario (modelo ProfileUser).
       Esto se puede hacer en panel de administrador o haciendo click en el enlace "nuevo record" del menú.
       Si el usuario no tiene el perfil diligenciado, se redirige al formulario para completarlo.

*CREACIÓN DE REGISTROS
    1) Cuando el ususario tiene su perfil completo, el mismo enlace "nuevo record" del menú, lo lleva a la
       vista de creación de registro. Acá se puede editar la información del usuario y se puede crear los registros.


*VISUALIZACIÓN Y BÚSQUEDA DE REGISTROS
    1) En la misma vista, al fondo de la página se muestra una tabla con todos los registros del ususario, la cual incluye
        enlaces para descargar el archivo que se subió en el registro.
    2)  Con el formulario de búsqueda se puede buscar en los registros del ususario. Los resultados se ven en la misma tabla.
       Para volver visualizar todos los registros nuevamente, se le da click en el ícono al lado del título "Borrar filtro"
