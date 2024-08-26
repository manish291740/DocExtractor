from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.conf import settings
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from PIL import Image
from pdf2image import convert_from_path
from .utils import OCRText, analyze_text_with_ai
import os, json
from .models import Document, ExtractedText, AIText
import threading
import queue
from .RegistrationForm import UserRegistrationForm
User = get_user_model()
document_queue = queue.Queue()
print("views +===",settings.POPPLER_PATH)
def initialize_workers():
    num_workers = 3  # Number of concurrent workers
    for _ in range(num_workers):
        worker = threading.Thread(target=process_documents_from_queue)
        worker.daemon = True
        worker.start()

def process_documents_from_queue():
    while True:
        document = document_queue.get()
        process_single_document(document)
        document_queue.task_done()

def process_single_document(document):
    try:
        document.status = 'processing'
        document.save()
        file_path = os.path.join('Documents/', document.file.name)
        text = ""

        if document.file.name.endswith('.pdf'):
            pages = convert_from_path(file_path, 300,
                                      poppler_path=settings.POPPLER_PATH)
            for page in pages:
                text += OCRText(page)

        elif document.file.name.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            image = Image.open(file_path)
            text = OCRText(image)

        else:
            document.status = 'error'
            document.save()
            return

        ExtractedText.objects.create(document=document, text=text)
        analyzetext = analyze_text_with_ai(text)

        AIText.objects.create(
            document=document,
            entity=json.dumps(analyzetext['NER']),
            classification=json.dumps(analyzetext['Classification']),
            sentiment=json.dumps(analyzetext['Sentiment'])
        )

        document.status = 'complete'
        document.save()

    except Exception as e:
        document.status = 'error'
        document.error = str(e)
        document.save()

initialize_workers()

@login_required
def upload_doc(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['fileInput']
        valid_mime_types = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf']
        documents = Document.objects.filter(user=request.user)

        if uploaded_file.content_type not in valid_mime_types:
            return render(request, 'upload.html', {'documents': documents,
                                                   'error': "Unsupported file type. Please upload an image or PDF file."})

        if uploaded_file.size > 2 * 1024 * 1024:
            return render(request, 'upload.html', {'documents': documents,
                                                   'error': "File too large. Size should not exceed 2 MiB."})

        # Save the file
        fs = FileSystemStorage(location='Documents/')
        filename = fs.save(uploaded_file.name, uploaded_file)

        new_document = Document(
            user=request.user,
            title=uploaded_file.name,
            file=filename,
            status='uploaded'
        )
        new_document.save()
        return redirect('/')
    documents = Document.objects.filter(user=request.user)
    return render(request, 'upload.html', {'documents': documents})

@login_required
def process_doc(request, doc_id):
    if request.method == "POST":
        document = get_object_or_404(Document, id=doc_id, user=request.user)
        document.status = 'queue'
        document.save()
        document_queue.put(document)
        return redirect('/')

@login_required
def view_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)

    if document.status == 'complete':
        extracted_text = get_object_or_404(ExtractedText, document=document)
        ai_text = get_object_or_404(AIText, document=document)

        entity_data = json.loads(ai_text.entity)
        classification_data = json.loads(ai_text.classification)
        sentiment_data = json.loads(ai_text.sentiment)

        context = {
            'extracted_text': extracted_text.text,
            'entity': entity_data,
            'classification': classification_data,
            'sentiment': sentiment_data,
        }
        return render(request, 'view_document.html', context)

    elif document.status == 'error':
        extracted_text = ExtractedText.objects.filter(document=document).first()
        context = {
            'error_message': document.error,
            'extracted_text': extracted_text.text if extracted_text else "No text extracted",
        }
        return render(request, 'view_error.html', context)

    else:
        return HttpResponse("Invalid document status.")

@login_required
def delete_document(request, document_id):
    if request.method == "POST":
        document = get_object_or_404(Document, id=document_id)

        if document.status in ['error', 'complete']:
            AIText.objects.filter(document=document).delete()
            ExtractedText.objects.filter(document=document).delete()
            document.delete()
        return redirect('upload_doc')

    return redirect('upload_doc')


def process(request):
    return HttpResponse("<h1>hello</h1>")

class CustomLogin(LoginView):
    template_name = 'Login.html'
    fields='__all__'
    redirect_authenticated_user = True
    def get_success_url(self):
        return reverse_lazy('upload_doc')

class Register(FormView):
    template_name = 'Register.html'
    form_class = UserRegistrationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('upload_doc')

    def form_valid(self, form):
        user = form.save(commit=False)

        print("password:--",form.cleaned_data)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        login(self.request, user)
        return super(Register, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('upload_doc')
        return super(Register, self).get(request, *args, **kwargs)