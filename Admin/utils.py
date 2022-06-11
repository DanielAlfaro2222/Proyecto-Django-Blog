from django.contrib.auth.mixins import UserPassesTestMixin


class AdminGroupTest(UserPassesTestMixin):
    """
    Clase para verificar si el usuario tiene el rol de administrador.
    """

    def test_func(self):
        # obtenemos todos los grupos del usuario logueado
        grupos = self.request.user.groups.filter(name='Administrador').exists()
        # comparamos que el usuario pertenezca al grupo Administrador
        if grupos:
            return True
        return False


class AuthorGroupTest(UserPassesTestMixin):
    """
    Clase para verificar si el usuario tiene el rol de autor.
    """

    def test_func(self):
        # obtenemos todos los grupos del usuario logueado
        grupos = self.request.user.groups.filter(name='Autor').exists()
        # comparamos que el usuario pertenezca al grupo Autor
        if grupos:
            return True
        return False
