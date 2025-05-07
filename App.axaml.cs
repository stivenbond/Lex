using System;
using System.IO;
using Avalonia;
using Avalonia.Controls.ApplicationLifetimes;
using Avalonia.Data.Core;
using Avalonia.Data.Core.Plugins;
using System.Linq;
using Avalonia.Markup.Xaml;
using Lex.Data;
using Lex.Data.Repositories;
using Lex.ViewModels;
using Lex.Views;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;

namespace Lex;

public partial class App : Application
{
    public IServiceProvider Services { get; private set; } = null!;


    public override void Initialize()
    {
        AvaloniaXamlLoader.Load(this);
    }

    public override void OnFrameworkInitializationCompleted()
    {
        var services = new ServiceCollection();
        
        var dataDir = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
        var appDataPath = Path.Combine(dataDir, "Lex");
        Directory.CreateDirectory(appDataPath); // Ensures the folder exists
        var dbPath = Path.Combine(appDataPath, "lex.db");

        //Add DbContext
        services.AddDbContext<AppDbContext>(options =>
            options.UseSqlite($"Data Source={dbPath}"));

        // Register repositories
        services.AddScoped<LessonRepository>();
        services.AddScoped<TestRepository>();
        services.AddScoped<QuestionRepository>();
        services.AddScoped<LessonFileRepository>();
        services.AddScoped<DiaryRepository>();
        services.AddScoped<SchoolClassRepository>();

        // Register view models
        services.AddTransient<LeftSidebarViewModel>();
        services.AddTransient<MainWindowViewModel>();

        // Register MainWindow with ViewModel injection
        services.AddTransient<MainWindow>(sp =>
            new MainWindow(sp.GetRequiredService<MainWindowViewModel>()));

        Services = services.BuildServiceProvider();
        
        using (var scope = Services.CreateScope())
        {
            var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
            db.Database.Migrate();
        }

        // Set up MainWindow startup
        if (ApplicationLifetime is IClassicDesktopStyleApplicationLifetime desktop)
        {
            desktop.MainWindow = Services.GetRequiredService<MainWindow>();
        }

        base.OnFrameworkInitializationCompleted();

    }

    private void DisableAvaloniaDataAnnotationValidation()
    {
        // Get an array of plugins to remove
        var dataValidationPluginsToRemove =
            BindingPlugins.DataValidators.OfType<DataAnnotationsValidationPlugin>().ToArray();

        // remove each entry found
        foreach (var plugin in dataValidationPluginsToRemove)
        {
            BindingPlugins.DataValidators.Remove(plugin);
        }
    }
}