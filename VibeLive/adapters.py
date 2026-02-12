from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        """
        Populate user fields from social login data.
        """
        user = super().populate_user(request, sociallogin, data)
        
        # Google specific extraction if missing
        extra_data = sociallogin.account.extra_data
        if not user.first_name:
            user.first_name = extra_data.get('given_name', data.get('first_name', ''))
        if not user.last_name:
            user.last_name = extra_data.get('family_name', data.get('last_name', ''))
            
        return user
