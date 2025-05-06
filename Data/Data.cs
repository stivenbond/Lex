using Lex.Models;
using Microsoft.EntityFrameworkCore;

namespace Lex.Data;

public class LexContext : DbContext
{
    public DbSet<Lesson> Lessons { get; set; }
    public DbSet<Test> Tests { get; set; }
    public DbSet<Question> Questions { get; set; }
    public DbSet<File> Files { get; set; }
    public DbSet<Diary> Diaries { get; set; }
    public DbSet<Class> Classes { get; set; }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        optionsBuilder.UseSqlite("Data Source=school.db");
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Lesson>()
            .HasMany(l => l.Tests)
            .WithOne(t => t.Lesson)
            .HasForeignKey(t => t.LessonId);

        modelBuilder.Entity<Lesson>()
            .HasMany(l => l.Files)
            .WithOne(f => f.Lesson)
            .HasForeignKey(f => f.LessonId);

        modelBuilder.Entity<Class>()
            .HasMany(c => c.Diaries)
            .WithOne(d => d.Class)
            .HasForeignKey(d => d.ClassToReference);

        modelBuilder.Entity<Class>()
            .HasOne(c => c.Lesson)
            .WithMany(l => l.Classes)
            .HasForeignKey(c => c.CurrentLesson);
    }
}
