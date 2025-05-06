using ReactiveUI;

namespace Lex.ViewModels
{
    public class WebReferenceViewModel : ViewModelBase
    {
        public required string _url;
        public string Url
        {
            get => _url;
            set => this.RaiseAndSetIfChanged(ref _url, value);
        }

        public WebReferenceViewModel()
        {
            Url = "https://avaloniaui.net/";
        }
    }
}