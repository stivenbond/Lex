using Avalonia.Controls;
using Avalonia.Markup.Xaml;
using Avalonia.ReactiveUI;
using Lex.ViewModels;
using ReactiveUI;

namespace Lex.Views
{
    public partial class TextDocumentView : ReactiveUserControl<TextDocumentViewModel>
    {
        public TextDocumentView()
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