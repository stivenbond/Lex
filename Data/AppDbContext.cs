using Microsoft.EntityFrameworkCore;
using Lex.Models;

namespace Lex.Data
{
    public class AppDbContext(DbContextOptions<AppDbContext> options) : DbContext(options)
    {

        public DbSet<Lesson> Lessons => Set<Lesson>();
        public DbSet<Test> Tests => Set<Test>();
        public DbSet<Question> Questions => Set<Question>();
        public DbSet<LessonFile> Files => Set<LessonFile>();
        public DbSet<Diary> Diaries => Set<Diary>();
        public DbSet<SchoolClass> Classes => Set<SchoolClass>();

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // LESSON
            modelBuilder.Entity<Lesson>(entity =>
            {
                entity.HasKey(l => l.LessonId);
                entity.Property(l => l.Topic).IsRequired().HasMaxLength(255);
                entity.Property(l => l.Subject).IsRequired().HasMaxLength(255);
                entity.Property(l => l.Content).IsRequired().HasColumnType("TEXT");
            });

            // TEST
            modelBuilder.Entity<Test>(entity =>
            {
                entity.HasKey(t => t.TestId);
                entity.HasOne(t => t.Lesson)
                      .WithMany(l => l.Tests)
                      .HasForeignKey(t => t.LessonId)
                      .OnDelete(DeleteBehavior.Cascade);
            });

            // QUESTION
            modelBuilder.Entity<Question>(entity =>
            {
                entity.HasKey(q => q.QuestionId);
                entity.Property(q => q.QuestionText).IsRequired().HasMaxLength(512);
                entity.Property(q => q.OptionA).IsRequired().HasMaxLength(512);
                entity.Property(q => q.OptionB).IsRequired().HasMaxLength(512);
                entity.Property(q => q.OptionC).IsRequired().HasMaxLength(512);
                entity.Property(q => q.OptionD).IsRequired().HasMaxLength(512);
                entity.Property(q => q.CorrectOption).IsRequired().HasColumnType("CHAR(1)");

                entity.HasOne(q => q.Test)
                      .WithMany(t => t.Questions)
                      .HasForeignKey(q => q.TestId)
                      .OnDelete(DeleteBehavior.Cascade);
            });

            // FILE
            modelBuilder.Entity<LessonFile>(entity =>
            {
                entity.HasKey(f => f.FileId);
                entity.Property(f => f.Type).IsRequired().HasMaxLength(255);
                entity.Property(f => f.Content).IsRequired(); // Blob is auto-handled

                entity.HasOne(f => f.Lesson)
                      .WithMany(l => l.Files)
                      .HasForeignKey(f => f.LessonId)
                      .OnDelete(DeleteBehavior.Cascade);
            });

            // DIARY
            modelBuilder.Entity<Diary>(entity =>
            {
                entity.HasKey(d => d.DiaryId);
                entity.Property(d => d.Content).IsRequired().HasColumnType("TEXT");
                entity.Property(d => d.SentOver).IsRequired();
                entity.Property(d => d.DateOfReference).IsRequired();

                entity.HasOne(d => d.Class)
                      .WithMany(c => c.Diaries)
                      .HasForeignKey(d => d.ClassToReference)
                      .OnDelete(DeleteBehavior.Cascade);
            });

            // CLASS
            modelBuilder.Entity<SchoolClass>(entity =>
            {
                entity.HasKey(c => c.ClassId);
                entity.Property(c => c.Subject).IsRequired().HasMaxLength(255);

                entity.HasOne(c => c.CurrentLesson)
                      .WithMany()
                      .HasForeignKey(c => c.CurrentLessonId)
                      .OnDelete(DeleteBehavior.SetNull);
            });
        }
    }
}
