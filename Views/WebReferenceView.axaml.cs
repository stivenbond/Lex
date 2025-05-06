using Avalonia.Controls;
using Avalonia.Markup.Xaml;
using Avalonia.ReactiveUI;
using Lex.ViewModels;
using ReactiveUI;

namespace Lex.Views
{
    public partial class WebReferenceView : ReactiveUserControl<WebReferenceViewModel>
    {
        public WebReferenceView()
        {
            InitializeComponent();
            this.WhenActivated(disposables => { });
        }

        private void InitializeComponent()
        {
            AvaloniaXamlLoader.Load(this);
        }
    }
}