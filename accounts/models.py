from re import I
from statistics import mode
from urllib import request
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.mail import EmailMessage
from django.dispatch import receiver
from django.db import models
# Create your models here.
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
from django.contrib.staticfiles import finders
from typing import Dict, Final, Optional


# Constants for sending password-reset emails.
LOGO_FILE_PATH: Final[str] = r"../static/logo-ventanilla.png"
LOGO_CID_NAME: Final[str] = "logo"
PASSWORD_RESET_FORM_TEMPLATE: Final[str] = "registration/password_reset_form.html"
PASSWORD_RESET_HTML_TEMPLATE: Final[str] = "registration/password_newuser_email.html"
PASSWORD_RESET_TEXT_TEMPLATE: Final[str] = "registration/password_reset_email.txt"
PASSWORD_RESET_SUBJECT_TEMPLATE: Final[str] = "registration/password_reset_subject.txt"
SUPPORT_EMAIL: Final[str] = "felipe.garzon@indepenmedia.co"
FROM_EMAIL: Final[str] = f"Soporte MyPartner <{SUPPORT_EMAIL}>"
YOUR_COMPANY_NAME: Final[str] = "My Partner"


def get_as_mime_image(image_file_path: str, cid_name: str) -> MIMEImage:
    """Fetch an image file and return it wrapped in a ``MIMEImage`` object for use 
    in emails.

    After the ``MIMEImage`` has been attached to an email, reference the image in 
    the HTML using the Content ID.

    Example:

    If the CID name is "logo", then the HTML reference would be:

    <img src="cid:logo" />

    Args:
        image_file_path: The path of the image. The path must be findable by the 
            Django staticfiles app.
        cid_name: The Content-ID name to use within the HTML email body to 
            reference the image.

    Raises:
        FileNotFoundError: If the image file cannot be found by the staticfiles app.

    Returns:
        MIMEImage: The image wrapped in a ``MIMEImage`` object and the Content ID 
        set to ``cid_name``.
    """
    paths = finders.find(image_file_path)
    if paths is None:
        raise FileNotFoundError(f"{image_file_path} not found in static files")

    if isinstance(paths, list):
        final_path = paths[0]
    else:
        final_path = paths
    with open(final_path, 'rb') as f:
        image_data = f.read()

    mime_image = MIMEImage(image_data)
    mime_image.add_header("Content-ID", f"<{cid_name}>")
    return mime_image

def send_mail(
        subject_template_name: str,
        email_template_name: str,
        context: Dict[str, str],
        from_email: Optional[str],
        to_email: str,
        html_email_template_name: Optional[str] = None,
    ) -> None:
        """Send a ``django.core.mail.EmailMultiAlternatives`` to ``to_email``.

        This method also attaches the company logo, which can be added to the 
        email HTML template using:

        <img src="cid:logo" />

        Args:
            subject_template_name: Path of the template to use as the email 
                subject.
            email_template_name: Path of the template to use for the plain text 
                email body.
            context: A context dictionary to use when rendering the password reset 
                email templates.
            from_email: The From email address.
            to_email: The To email address.
            html_email_template_name: Optional; Path of the template to use for 
                the HTML email body. Defaults to None.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, 
                                               from_email=from_email, to=[to_email],
                                               reply_to=[from_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')
            email_message.mixed_subtype = "related"
            mime_image = get_as_mime_image(image_file_path=LOGO_FILE_PATH, cid_name=LOGO_CID_NAME)
            email_message.attach(mime_image)  # type: ignore

        email_message.send()


@receiver(models.signals.post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):    
    if created:        
        #current_site = Site.objects.get_current()
        site_name = 'Ventanilla virtual' #current_site.name
        domain = '127.0.0.1:8000' #current_site.domain
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(instance)
        subject = 'Bienvenido al Ventanilla virtual'
        #message = 'Welcome to the site'
        use_https = None
        extra_email_context = None
        context = {
                'email': sender.email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(instance.pk)),
                'user': instance,
                'token': token,
                'protocol': 'https' if use_https else 'http',
                **(extra_email_context or {}),
            }
    
        email_template_name = PASSWORD_RESET_TEXT_TEMPLATE
        from_email = FROM_EMAIL
        html_email_template_name = PASSWORD_RESET_HTML_TEMPLATE
        subject_template_name = PASSWORD_RESET_SUBJECT_TEMPLATE

        send_mail(
            subject_template_name = subject_template_name,
            email_template_name = email_template_name,
            context = context,
            from_email = from_email,
            to_email = instance.email,
            html_email_template_name = html_email_template_name
            )


class Company(models.Model):
    companyid = models.CharField(max_length=20, blank=False, null=False, verbose_name='ID Empresa')
    companyname = models.CharField(max_length=250, blank=False, null=False, verbose_name='Nombre de Empresa')

    class Meta:
        db_table = 'mvnt_company'
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'

    def __str__(self):
        return self.companyname


class Profile(models.Model):
    companyid = models.ForeignKey(Company, on_delete=models.CASCADE, default=1)
    user = models.OneToOneField(User, on_delete=models.CASCADE)    
    numberId = models.CharField(max_length=30, verbose_name='Número de identificación')
    taxNumberType = models.CharField(max_length=30, choices=[('CC', 'Cédula de ciudadanía'), ('NIT', 'Número de Identificación Tributaria')], verbose_name='Tipo de identificación')
    is_document_manager = models.BooleanField(default=False, verbose_name='Gestor Documental')
    is_active = models.BooleanField(default=False, verbose_name='Usuario activado')

    class Meta:
        db_table = 'mvnt_profile'
        verbose_name = 'Perfil de usuario'
        verbose_name_plural = 'Perfiles de usuario'

    def __str__(self):
        return self.user.username