# test forms
class UserFormTests(TestCase):
    ''' test out all the forms '''

    def test_SignUpForm_valid(self):
        form = SignUpForm(data=sign_up_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.cleaned_data['username'], 
                        'stuartgorodonmcintosh')

    def test_SignUpForm_not_valid(self):
        form = SignUpForm(data=user_data)
        self.assertFalse(form.is_valid())
        self.assertTrue({'password_mismatch': 
                         "The two password fields didn't match."},
                        form.error_messages
                        )

    def test_EditProfileForm_valid(self):
        form = EditProfileForm(data=edit_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.cleaned_data['bio'], 
                        'this is my life version 2')

    def test_UserUpdateForm_valid(self):
        form = UserUpdateForm(data=update_data)
        self.assertTrue(form.is_valid())
