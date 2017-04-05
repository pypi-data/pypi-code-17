from django.test import TestCase
from users.models import AdminUser, LeaderUser, MemberUser, User, Project, Role
from users.Claudia.user_form import AdminUserForm, AdminUpdateForm, UserUpdateForm


class AdminModelTest(TestCase):
    def setUp(self):
        adm01 = AdminUser.objects.create_user(username='12341234', first_name='Aaron', last_name='Hotchner', email='aaron_hotchner@gmail.com', phone='88770000')
        adm01.save()
        adm02 = AdminUser.objects.create_user(username='22334455', first_name='Megan', last_name='Smith', email='megan_smith@gmail.com', phone='98701122')
        adm02.save()

    def test_phone_max_length(self):
        user = AdminUser.objects.get(pk=2)
        max_length = user._meta.get_field('phone').max_length
        self.assertEquals(max_length, 15)


class AdminUserFormTest(TestCase):
    def test_invalid_adminuser_form(self):
        username = "12345678900"
        first_name = "Megan"
        last_name = "Smith"
        email = "megan_smith@gmail.com"
        password = "qwerty123"
        phone = "98790001"
        bio = "Test"
        form_data = {'username': username, 'first_name': first_name, 'last_name': last_name, 'email': email,
                     'password': password, 'phone': phone, 'bio': bio}
        form = AdminUserForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_valid_adminuser_form(self):
        username = "12345678"
        first_name = "Megan"
        last_name = "Smith"
        email = "megan_smith@gmail.com"
        password = "qwerty123"
        phone = "98790001"
        bio = "Test"
        form_data = {'username': username, 'first_name': first_name, 'last_name': last_name, 'email': email,
                     'password': password, 'phone': phone, 'bio': bio}
        form = AdminUserForm(data=form_data)
        self.assertTrue(form.is_valid())


class AdminUpdateFormTest(TestCase):
    def setUp(self):
        adm01 = AdminUser.objects.create_user(username='12341234', first_name='Aaron', last_name='Hotchner', email='aaron_hotchner@gmail.com', phone='88770000')
        adm01.save()
        adm02 = AdminUser.objects.create_user(username='22334455', first_name='Megan', last_name='Smith', email='megan_smith@gmail.com', phone='98701122')
        adm02.save()

    def test_invalid_adminupdate_form(self):
        user = AdminUser.objects.get(pk=2)
        num = '202-555-0137-019890'
        form_data = {'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email, 'phone': num}
        form = AdminUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_valid_adminupdate_form(self):
        user = AdminUser.objects.get(pk=2)
        email = 'derek_morgan@gmail.com'
        num = '8555-0137'
        form_data = {'first_name': user.first_name, 'last_name': user.last_name, 'email': email, 'phone': num}
        form = AdminUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())


class UserUpdateFormTest(TestCase):
    def setUp(self):
        adm = AdminUser.objects.create_user(username='G8009720', first_name='Derek', last_name='Morgan', email='derek_morgan@gmail.com', phone='97706000')
        adm.save()
        lead = LeaderUser.objects.create_user(username='12341234', first_name='Aaron', last_name='Hotchner', email='aaron_hotchner@gmail.com', phone='88770000')
        lead.save()

    def test_invalid_userupdate_form(self):
        user = User.objects.get(first_name__iexact='Derek')
        num = '202-555-0137-019890'
        form_data = {'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email, 'phone': num}
        form = UserUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_valid_userupdate_form(self):
        user = User.objects.get(first_name__iexact='Aaron')
        num = '202-555-0137'
        email = 'aaron_hotchner@example.com'
        form_data = {'first_name': user.first_name, 'last_name': user.last_name, 'email': email, 'phone': num}
        form = UserUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())


class CreateAdminUserViewTest(TestCase):
    def setUp(self):
        adm = AdminUser.objects.create_user(username='G8009720', first_name='Derek', last_name='Morgan',
                                            password='qwerty123', email='derek_morgan@gmail.com', phone='97706000')
        adm.save()

    def test_create_admin_view(self):
        user_login = self.client.login(username='G8009720', password='qwerty123')
        self.assertTrue(user_login)
        response = self.client.get('/admin_user/G8009720/add_admin/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/adminuser_form.html')


class GetAdminDetailViewTest(TestCase):
    def setUp(self):
        adm = AdminUser.objects.create_user(username='G8009720', first_name='Derek', last_name='Morgan',
                                            password='qwerty123', email='derek_morgan@gmail.com', phone='97706000')
        adm.save()

    def test_get_admin_detail_view(self):
        user_login = self.client.login(username='G8009720', password='qwerty123')
        self.assertTrue(user_login)
        response = self.client.get('/admin_user/G8009720/details/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_information.html')


class UpdateAdminDetailViewTest(TestCase):
    def setUp(self):
        adm = AdminUser.objects.create_user(username='G8009720', first_name='Derek', last_name='Morgan',
                                            password='qwerty123', email='derek_morgan@gmail.com', phone='97706000')
        adm.save()

    def test_update_admin_detail_view(self):
        user_login = self.client.login(username='G8009720', password='qwerty123')
        self.assertTrue(user_login)
        response = self.client.get('/admin_user/G8009720/update/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/update_admin_form.html')


class DisplayAllProjectsViewTest(TestCase):
    def setUp(self):
        adm = AdminUser.objects.create_user(username='G8009720', first_name='Derek', last_name='Morgan',
                                            password='qwerty123', email='derek_morgan@gmail.com', phone='97706000')
        adm.save()

    def test_display_all_projects_view(self):
        user_login = self.client.login(username='G8009720', password='qwerty123')
        self.assertTrue(user_login)
        response = self.client.get('/admin_user/G8009720/project/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/all_project_list.html')


class DisplayOpenProjectsViewTest(TestCase):
    def setUp(self):
        adm = AdminUser.objects.create_user(username='G8009720', first_name='Derek', last_name='Morgan',
                                            password='qwerty123', email='derek_morgan@gmail.com', phone='97706000')
        adm.save()

    def test_display_open_projects_view(self):
        user_login = self.client.login(username='G8009720', password='qwerty123')
        self.assertTrue(user_login)
        response = self.client.get('/admin_user/G8009720/open_project/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/open_project_list.html')


class DisplayProjectInformationViewTest(TestCase):
    def setUp(self):
        adm = AdminUser.objects.create_user(username='G8009720', first_name='Derek', last_name='Morgan',
                                            password='qwerty123', email='derek_morgan@gmail.com', phone='97706000')
        adm.save()
        lead = LeaderUser.objects.create_user(username='12341234', first_name='Aaron', last_name='Hotchner',
                                              password='qwerty123', email='aaron_hotchner@gmail.com', phone='88770000')
        lead.save()
        project = Project.objects.create(name='PMT', start_date='2017-03-01', end_date='2017-03-30', leader_id=lead.id)
        project.admins.add(adm)
        project.save()

    def test_display_project_information_view(self):
        user_login = self.client.login(username='G8009720', password='qwerty123')
        self.assertTrue(user_login)
        response = self.client.get('/admin_user/G8009720/PMT/project_detail/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/project_information.html')


class UserUpdateViewTest(TestCase):
    def setUp(self):
        adm = AdminUser.objects.create_user(username='G8009720', first_name='Derek', last_name='Morgan',
                                            password='qwerty123', email='derek_morgan@gmail.com', phone='97706000')
        adm.save()
        lead = LeaderUser.objects.create_user(username='12341234', first_name='Aaron', last_name='Hotchner',
                                              password='qwerty123', email='aaron_hotchner@gmail.com', phone='88770000')
        lead.save()
        project = Project.objects.create(name='PMT', start_date='2017-03-01', end_date='2017-03-30', leader_id=lead.id)
        project.admins.add(adm)
        project.save()
        role = Role.objects.create(title='Security Coordinator')
        role.save()
        mem = MemberUser.objects.create_user(username='67091200', first_name='Spencer', last_name='Reid',
                                             password='qwerty123', email='spencer_reid@gmail.com', phone='88779876',
                                             role_id=role.id, project_id=project.id)
        mem.save()

    def test_user_update_view(self):
        user_login = self.client.login(username='G8009720', password='qwerty123')
        self.assertTrue(user_login)
        response = self.client.get('/admin_user/G8009720/update_user/12341234/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_update_form.html')


class DeleteAUserViewTest(TestCase):
    def setUp(self):
        adm = AdminUser.objects.create_user(username='G8009720', first_name='Derek', last_name='Morgan',
                                            password='qwerty123', email='derek_morgan@gmail.com', phone='97706000')
        adm.save()
        lead = LeaderUser.objects.create_user(username='12341234', first_name='Aaron', last_name='Hotchner',
                                              password='qwerty123', email='aaron_hotchner@gmail.com', phone='88770000')
        lead.save()

    def test_delete_a_user_view(self):
        user_login = self.client.login(username='G8009720', password='qwerty123')
        self.assertTrue(user_login)
        response = self.client.get('/admin_user/G8009720/delete/12341234/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/admin_user/G8009720/list/')


class DisplayListOfUsersViewTest(TestCase):
    def setUp(self):
        adm = AdminUser.objects.create_user(username='G8009720', first_name='Derek', last_name='Morgan',
                                            password='qwerty123', email='derek_morgan@gmail.com', phone='97706000')
        adm.save()

    def test_display_list_of_users_view(self):
        user_login = self.client.login(username='G8009720', password='qwerty123')
        self.assertTrue(user_login)
        response = self.client.get('/admin_user/G8009720/list/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/list_of_users.html')


class GetUserDetailViewTest(TestCase):
    def setUp(self):
        adm = AdminUser.objects.create_user(username='G8009720', first_name='Derek', last_name='Morgan',
                                            password='qwerty123', email='derek_morgan@gmail.com', phone='97706000')
        adm.save()
        lead = LeaderUser.objects.create_user(username='12341234', first_name='Aaron', last_name='Hotchner',
                                              password='qwerty123', email='aaron_hotchner@gmail.com', phone='88770000')
        lead.save()

    def test_get_user_detail_view_test(self):
        user_login = self.client.login(username='G8009720', password='qwerty123')
        self.assertTrue(user_login)
        response = self.client.get('/admin_user/G8009720/user_detail/12341234/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_information.html')


class SearchUsersViewTest(TestCase):
    def setUp(self):
        adm = AdminUser.objects.create_user(username='G8009720', first_name='Derek', last_name='Morgan',
                                            password='qwerty123', email='derek_morgan@gmail.com', phone='97706000')
        adm.save()

    def test_search_users_view(self):
        user_login = self.client.login(username='G8009720', password='qwerty123')
        self.assertTrue(user_login)
        response = self.client.get('/admin_user/G8009720/search/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/search.html')


class DeleteProjectViewTest(TestCase):
    def setUp(self):
        adm = AdminUser.objects.create_user(username='G8009720', first_name='Derek', last_name='Morgan',
                                            password='qwerty123', email='derek_morgan@gmail.com', phone='97706000')
        adm.save()
        lead = LeaderUser.objects.create_user(username='12341234', first_name='Aaron', last_name='Hotchner',
                                              password='qwerty123', email='aaron_hotchner@gmail.com', phone='88770000')
        lead.save()
        project = Project.objects.create(name='PMT', start_date='2017-03-01', end_date='2017-03-30', leader_id=lead.id)
        project.admins.add(adm)
        project.save()

    def test_delete_project_view(self):
        user_login = self.client.login(username='G8009720', password='qwerty123')
        self.assertTrue(user_login)
        response = self.client.get('/admin_user/G8009720/delete_project/PMT/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/admin_user/G8009720/project/')