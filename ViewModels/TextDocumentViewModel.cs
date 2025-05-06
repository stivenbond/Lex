using ReactiveUI;
namespace Lex.ViewModels
{
    public class TextDocumentViewModel : ViewModelBase
    {
        public required string _documentText;
        public string DocumentText
        {
            get => _documentText;
            set => this.RaiseAndSetIfChanged(ref _documentText, value);
        }

        public TextDocumentViewModel()
        {
            DocumentText = "This is a text document.";
        }
    }
}