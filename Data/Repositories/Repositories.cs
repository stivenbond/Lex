// Assumes namespace: YourAppNamespace.Data

using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using DynamicData;
using Lex.Models;
using Microsoft.EntityFrameworkCore;
using ReactiveUI;

namespace Lex.Data.Repositories
{
    public interface IRepository<T> where T : class
    {
        IObservable<IChangeSet<T>> Connect();
        Task<IReadOnlyList<T>> GetAllAsync();
        Task<T?> GetByIdAsync(int id);
        Task AddAsync(T entity);
        Task UpdateAsync(T entity);
        Task DeleteAsync(T entity);
    }

    public abstract class ReactiveRepository<T>(AppDbContext context) : ReactiveObject, IRepository<T>
        where T : class
    {
        private readonly SourceList<T> _items = new();

        public IObservable<IChangeSet<T>> Connect() => _items.Connect();

        public virtual async Task<IReadOnlyList<T>> GetAllAsync()
        {
            var items = await context.Set<T>().ToListAsync();
            _items.Edit(inner =>
            {
                inner.Clear();
                inner.AddRange(items);
            });
            return items;
        }

        public virtual async Task<T?> GetByIdAsync(int id)
        {
            return await context.Set<T>().FindAsync(id);
        }

        public virtual async Task AddAsync(T entity)
        {
            context.Set<T>().Add(entity);
            await context.SaveChangesAsync();
            _items.Add(entity);
        }

        public virtual async Task UpdateAsync(T entity)
        {
            context.Set<T>().Update(entity);
            await context.SaveChangesAsync();
            await RefreshListAsync();
        }

        public virtual async Task DeleteAsync(T entity)
        {
            context.Set<T>().Remove(entity);
            await context.SaveChangesAsync();
            _items.Remove(entity);
        }

        protected virtual async Task RefreshListAsync()
        {
            var list = await context.Set<T>().ToListAsync();
            _items.Edit(inner =>
            {
                inner.Clear();
                inner.AddRange(list);
            });
        }
    }

    // Example: Specific repository for Lessons
    public class LessonRepository(AppDbContext context) : ReactiveRepository<Lesson>(context);

    public class TestRepository(AppDbContext context) : ReactiveRepository<Test>(context);

    public class QuestionRepository(AppDbContext context) : ReactiveRepository<Question>(context);

    public class LessonFileRepository(AppDbContext context) : ReactiveRepository<LessonFile>(context);

    public class DiaryRepository(AppDbContext context) : ReactiveRepository<Diary>(context);

    public class SchoolClassRepository(AppDbContext context) : ReactiveRepository<SchoolClass>(context);
}
