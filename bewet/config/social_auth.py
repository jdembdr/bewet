SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
)

#----------------
# registration config

ACCOUNT_ACTIVATION_DAYS=7

#----------------
# registration config
LOGIN_REDIRECT_URL = '/welcome/'


SOCIAL_AUTH_TWITTER_KEY = 'ZQJnkKF5HBvBUXdjftK7YJk25'
SOCIAL_AUTH_TWITTER_SECRET = 'SVytv6XYyi19FdHleOYiExihMutAuvi5eH267jIuj8ijBdiqqU'

SOCIAL_AUTH_FACEBOOK_KEY = '252475625125931'
SOCIAL_AUTH_FACEBOOK_SECRET = '30bd754279227774f935921904fc0655'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
  'locale': 'fr_FR',
  'fields': 'id, name, email, age_range'
}

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '568555224092-hdc0fn7fr1g17b00doku2rnrv1ggs1vb.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'NOW8muTbGQajglB5kleV_D2B'

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/welcome/'
SOCIAL_AUTH_LOGIN_URL = '/'


