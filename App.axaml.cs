using Avalonia;
using Avalonia.Controls.ApplicationLifetimes;
using Avalonia.Markup.Xaml;
using Lex.ViewModels;
using Lex.Views;

namespace Lex
{
    public partial class App : Application
    {
        public override void Initialize()
        {
            AvaloniaXamlLoader.Load(this);
        }

        public override void OnFrameworkInitializationCompleted()
        {
            if (ApplicationLifetime is IClassicDesktopStyleApplicationLifetime desktop)
            {
                desktop.MainWindow = new MainWindow
                {
                    DataContext = new MainWindowViewModel
                    {
                        _isSplitView = false,
                        _isLeftSidebarVisible = false,
                        _isRightSidebarVisible = false,
                        _leftContentViewModel = null,
                        _rightContentViewModel = null
                    },
                };
            }

            base.OnFrameworkInitializationCompleted();
        }
    }
}