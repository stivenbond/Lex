using Avalonia.Controls;
using Avalonia.ReactiveUI;
using Lex.ViewModels;
using ReactiveUI;

namespace Lex.Views
{
    public partial class MainWindow : ReactiveWindow<MainWindowViewModel>
    {
        public MainWindow()
        {
            InitializeComponent();
            this.WhenActivated(disposables => { });
        }
    }
}